// ==UserScript==
// @name         Qwen PreMod
// @namespace    HORSELOCK.qwen
// @version      1.0.0
// @description  Hides moderation visual effects. Prevents deletion of streaming response. Saves responses to GM storage and injects them into loaded conversations based on message ID.
// @match        *://qwen.ai/*
// @match        *://*.qwen.ai/*
// @match        *://chat.qwen.ai/*
// @downloadURL
// @updateURL
// @run-at       document-start
// @grant        GM.getValue
// @grant        GM.setValue
// ==/UserScript==

(function() {
    'use strict';

    function showBanner(message, { color = '#4A5568', duration = 4000 } = {}) {
        document.getElementById('qwen-premod-banner')?.remove();

        const banner = document.createElement('div');
        banner.id = 'qwen-premod-banner';
        banner.textContent = message;
        banner.style.backgroundColor = color;
        document.body.appendChild(banner);

        setTimeout(() => banner.classList.add('visible'), 10);

        setTimeout(() => {
            banner.classList.remove('visible');
            banner.addEventListener('transitionend', () => banner.remove());
        }, duration);
    }

    function whenReady(callback) {
        if (document.readyState !== 'loading') callback();
        else document.addEventListener('DOMContentLoaded', callback);
    }

    whenReady(() => {
        const style = document.createElement('style');
        style.textContent = `#qwen-premod-banner{position:fixed;top:15px;left:50%;transform:translateX(-50%);padding:10px 18px;border-radius:6px;color:#fff;box-shadow:0 3px 10px #0005;z-index:9999;opacity:0;transition:opacity .4s ease,top .4s ease;pointer-events:none}#qwen-premod-banner.visible{top:25px;opacity:1}`;
        document.head.appendChild(style);
        showBanner('Qwen PreMod Active', { color: '#722ed1', duration: 3000 });
    });

    function unBlock(moderationResult) {
        if (!moderationResult || !moderationResult.blocked) return false;
        const wasBlocked = moderationResult.blocked;
        moderationResult.blocked = false;
        return wasBlocked;
    }

    function checkModerationFlags(obj) {
        // Check various moderation flag patterns that Qwen might use
        if (!obj) return false;

        const flags = [
            'blocked', 'moderation', 'filtered', 'censored',
            'is_blocked', 'is_moderated', 'is_filtered'
        ];

        let wasBlocked = false;
        for (const flag of flags) {
            if (obj[flag] === true) {
                obj[flag] = false;
                wasBlocked = true;
            }
        }

        // Check for nested moderation objects
        if (obj.moderation_response) {
            wasBlocked = unBlock(obj.moderation_response) || wasBlocked;
        }
        if (obj.moderation_result) {
            wasBlocked = unBlock(obj.moderation_result) || wasBlocked;
        }

        return wasBlocked;
    }

    const pageGlobal = (typeof unsafeWindow !== 'undefined') ? unsafeWindow : window;
    const originalFetch = pageGlobal.fetch;

    pageGlobal.fetch = async function(...args) {
        const url = (typeof args[0] === 'string') ? args[0] : args[0]?.url;

        // Intercept Qwen API calls (adjust pattern based on actual API endpoints)
        // Common patterns: /api/chat, /api/conversation, /v1/chat, etc.
        if (!url || !/\/(api|v1)\/(chat|conversation|message)/.test(url)) {
            return originalFetch.call(pageGlobal, ...args);
        }

        const originalResponse = await originalFetch.call(pageGlobal, ...args);
        const contentType = originalResponse.headers.get('content-type') || '';

        // Handle streaming responses
        if (contentType.includes('text/event-stream') || contentType.includes('stream')) {
            let currentMessageId = null;
            let accumulatedContent = "";

            const stream = new ReadableStream({
                async start(controller) {
                    const reader = originalResponse.body.getReader();
                    const dec = new TextDecoder();
                    const enc = new TextEncoder();

                    while (true) {
                        const { done, value } = await reader.read();
                        if (done) {
                            if (currentMessageId && accumulatedContent) {
                                try {
                                    await GM.setValue(`qwen_msg_${currentMessageId}`, accumulatedContent);
                                } catch (e) {
                                    console.error("Qwen PreMod: Error saving to GM storage", e);
                                }
                            }
                            controller.close();
                            break;
                        }

                        const rawChunk = dec.decode(value, { stream: true });
                        const lines = rawChunk.split('\n');
                        const processedChunkLines = [];

                        for (const line of lines) {
                            if (line.startsWith('data: ') && line !== 'data: [DONE]') {
                                let jsonDataString = line.substring(5).trim();
                                try {
                                    let dataObj = JSON.parse(jsonDataString);

                                    // Extract message ID (various possible field names)
                                    if (!currentMessageId) {
                                        currentMessageId = dataObj.message_id || dataObj.id || dataObj.msg_id || dataObj.response_id;
                                    }

                                    // Check for moderation and unblock
                                    if (checkModerationFlags(dataObj)) {
                                        showBanner('Response moderated, saved it for you =)', { color: '#dd6b20' });
                                        jsonDataString = JSON.stringify(dataObj);
                                    }

                                    // Accumulate content from various possible fields
                                    if (dataObj.content) {
                                        accumulatedContent += dataObj.content;
                                    } else if (dataObj.text) {
                                        accumulatedContent += dataObj.text;
                                    } else if (dataObj.delta) {
                                        accumulatedContent += dataObj.delta;
                                    } else if (dataObj.choices && dataObj.choices[0]) {
                                        const choice = dataObj.choices[0];
                                        if (choice.delta && choice.delta.content) {
                                            accumulatedContent += choice.delta.content;
                                        } else if (choice.text) {
                                            accumulatedContent += choice.text;
                                        }
                                    }

                                } catch (e) {
                                    console.error('Qwen PreMod: Error processing line:', line, e);
                                } finally {
                                    processedChunkLines.push('data: ' + jsonDataString);
                                }
                            } else {
                                processedChunkLines.push(line);
                            }
                        }
                        controller.enqueue(enc.encode(processedChunkLines.join('\n')));
                    }
                }
            });

            return new Response(stream, {
                headers: originalResponse.headers,
                status: originalResponse.status,
                statusText: originalResponse.statusText
            });

        } else if (contentType.includes('application/json')) {
            // Handle JSON responses
            let jsonDataString = await originalResponse.text();
            let modified = false;

            try {
                let jsonData = JSON.parse(jsonDataString);

                // Handle moderation results in various formats
                if (jsonData.moderation_results) {
                    for (const modResult of jsonData.moderation_results) {
                        if (checkModerationFlags(modResult)) {
                            modified = true;
                            const messageId = modResult.message_id || modResult.id;
                            if (messageId) {
                                const storedContent = await GM.getValue(`qwen_msg_${messageId}`);
                                if (storedContent && jsonData.messages) {
                                    // Find and restore the message
                                    for (const msg of jsonData.messages) {
                                        if (msg.id === messageId || msg.message_id === messageId) {
                                            msg.content = storedContent;
                                            msg.text = storedContent;
                                        }
                                    }
                                }
                            }
                        }
                    }
                }

                // Check top-level moderation flags
                if (checkModerationFlags(jsonData)) {
                    modified = true;
                    showBanner('Response moderated, content preserved', { color: '#dd6b20' });
                }

                // Check messages array for moderation
                if (jsonData.messages) {
                    for (const message of jsonData.messages) {
                        if (checkModerationFlags(message)) {
                            modified = true;
                        }
                    }
                }

                if (modified) {
                    jsonDataString = JSON.stringify(jsonData);
                }

            } catch (e) {
                console.error("Qwen PreMod: Error processing JSON", e);
            } finally {
                return new Response(jsonDataString, {
                    headers: originalResponse.headers,
                    status: originalResponse.status,
                    statusText: originalResponse.statusText
                });
            }
        }

        return originalResponse;
    };
})();
