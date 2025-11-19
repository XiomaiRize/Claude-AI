// ==UserScript==
// @name         Qwen Shield
// @namespace    SHIELD.qwen
// @version      2.0.0
// @description  Multi-layered protection: DOM monitoring, IndexedDB backup, visual recovery panel, WebSocket interception, and auto-export
// @match        *://qwen.ai/*
// @match        *://*.qwen.ai/*
// @match        *://tongyi.aliyun.com/*
// @match        *://*.aliyun.com/qwen*
// @run-at       document-start
// @grant        GM.getValue
// @grant        GM.setValue
// @grant        GM.deleteValue
// @grant        unsafeWindow
// ==/UserScript==

(function() {
    'use strict';

    // ==================== CORE STORAGE SYSTEM ====================
    class QwenShieldDB {
        constructor() {
            this.dbName = 'QwenShieldDB';
            this.version = 1;
            this.db = null;
            this.init();
        }

        async init() {
            return new Promise((resolve, reject) => {
                const request = indexedDB.open(this.dbName, this.version);

                request.onerror = () => reject(request.error);
                request.onsuccess = () => {
                    this.db = request.result;
                    resolve(this.db);
                };

                request.onupgradeneeded = (event) => {
                    const db = event.target.result;

                    // Store for original messages before moderation
                    if (!db.objectStoreNames.contains('messages')) {
                        const msgStore = db.createObjectStore('messages', { keyPath: 'id' });
                        msgStore.createIndex('timestamp', 'timestamp', { unique: false });
                        msgStore.createIndex('conversationId', 'conversationId', { unique: false });
                    }

                    // Store for filtered/deleted content
                    if (!db.objectStoreNames.contains('filtered')) {
                        const filterStore = db.createObjectStore('filtered', { keyPath: 'id', autoIncrement: true });
                        filterStore.createIndex('messageId', 'messageId', { unique: false });
                        filterStore.createIndex('timestamp', 'timestamp', { unique: false });
                    }

                    // Store for conversation exports
                    if (!db.objectStoreNames.contains('exports')) {
                        db.createObjectStore('exports', { keyPath: 'id', autoIncrement: true });
                    }
                };
            });
        }

        async saveMessage(messageId, content, metadata = {}) {
            if (!this.db) await this.init();

            const transaction = this.db.transaction(['messages'], 'readwrite');
            const store = transaction.objectStore('messages');

            const data = {
                id: messageId,
                content: content,
                timestamp: Date.now(),
                conversationId: metadata.conversationId || 'unknown',
                metadata: metadata
            };

            return new Promise((resolve, reject) => {
                const request = store.put(data);
                request.onsuccess = () => resolve(data);
                request.onerror = () => reject(request.error);
            });
        }

        async getMessage(messageId) {
            if (!this.db) await this.init();

            const transaction = this.db.transaction(['messages'], 'readonly');
            const store = transaction.objectStore('messages');

            return new Promise((resolve, reject) => {
                const request = store.get(messageId);
                request.onsuccess = () => resolve(request.result);
                request.onerror = () => reject(request.error);
            });
        }

        async saveFiltered(messageId, originalContent, filteredContent, reason = '') {
            if (!this.db) await this.init();

            const transaction = this.db.transaction(['filtered'], 'readwrite');
            const store = transaction.objectStore('filtered');

            const data = {
                messageId: messageId,
                originalContent: originalContent,
                filteredContent: filteredContent,
                reason: reason,
                timestamp: Date.now()
            };

            return new Promise((resolve, reject) => {
                const request = store.add(data);
                request.onsuccess = () => resolve(data);
                request.onerror = () => reject(request.error);
            });
        }

        async getAllFiltered() {
            if (!this.db) await this.init();

            const transaction = this.db.transaction(['filtered'], 'readonly');
            const store = transaction.objectStore('filtered');

            return new Promise((resolve, reject) => {
                const request = store.getAll();
                request.onsuccess = () => resolve(request.result);
                request.onerror = () => reject(request.error);
            });
        }
    }

    const shieldDB = new QwenShieldDB();

    // ==================== UI COMPONENTS ====================
    class ShieldUI {
        constructor() {
            this.panelVisible = false;
            this.stats = { saved: 0, filtered: 0, intercepted: 0 };
            this.init();
        }

        init() {
            this.injectStyles();
            this.createFloatingButton();
            this.createRecoveryPanel();
        }

        injectStyles() {
            const style = document.createElement('style');
            style.textContent = `
                #qwen-shield-btn {
                    position: fixed;
                    bottom: 20px;
                    right: 20px;
                    width: 56px;
                    height: 56px;
                    border-radius: 50%;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    border: none;
                    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
                    cursor: pointer;
                    z-index: 999999;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-size: 24px;
                    transition: all 0.3s ease;
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                }

                #qwen-shield-btn:hover {
                    transform: scale(1.1);
                    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
                }

                #qwen-shield-btn .badge {
                    position: absolute;
                    top: -5px;
                    right: -5px;
                    background: #ff4757;
                    color: white;
                    border-radius: 12px;
                    padding: 2px 6px;
                    font-size: 11px;
                    font-weight: bold;
                    min-width: 18px;
                    text-align: center;
                }

                #qwen-shield-panel {
                    position: fixed;
                    top: 0;
                    right: -400px;
                    width: 400px;
                    height: 100vh;
                    background: #1a1a2e;
                    box-shadow: -5px 0 25px rgba(0, 0, 0, 0.3);
                    z-index: 999998;
                    transition: right 0.3s ease;
                    display: flex;
                    flex-direction: column;
                    color: #eee;
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                }

                #qwen-shield-panel.visible {
                    right: 0;
                }

                .shield-header {
                    padding: 20px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }

                .shield-header h2 {
                    margin: 0;
                    font-size: 20px;
                    color: white;
                }

                .shield-close {
                    background: none;
                    border: none;
                    color: white;
                    font-size: 24px;
                    cursor: pointer;
                    padding: 0;
                    width: 30px;
                    height: 30px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    border-radius: 50%;
                    transition: background 0.2s;
                }

                .shield-close:hover {
                    background: rgba(255, 255, 255, 0.2);
                }

                .shield-stats {
                    padding: 15px 20px;
                    background: #16213e;
                    display: grid;
                    grid-template-columns: repeat(3, 1fr);
                    gap: 10px;
                }

                .stat-item {
                    text-align: center;
                    padding: 10px;
                    background: #0f3460;
                    border-radius: 8px;
                }

                .stat-value {
                    font-size: 24px;
                    font-weight: bold;
                    color: #667eea;
                }

                .stat-label {
                    font-size: 11px;
                    color: #aaa;
                    margin-top: 5px;
                }

                .shield-content {
                    flex: 1;
                    overflow-y: auto;
                    padding: 20px;
                }

                .filtered-item {
                    background: #16213e;
                    border-radius: 8px;
                    padding: 15px;
                    margin-bottom: 15px;
                    border-left: 4px solid #ff4757;
                }

                .filtered-time {
                    font-size: 11px;
                    color: #888;
                    margin-bottom: 8px;
                }

                .filtered-content {
                    background: #0f3460;
                    padding: 10px;
                    border-radius: 6px;
                    font-size: 13px;
                    line-height: 1.6;
                    max-height: 150px;
                    overflow-y: auto;
                    white-space: pre-wrap;
                    word-wrap: break-word;
                }

                .shield-actions {
                    padding: 15px 20px;
                    background: #16213e;
                    display: flex;
                    gap: 10px;
                }

                .shield-btn {
                    flex: 1;
                    padding: 10px;
                    border: none;
                    border-radius: 6px;
                    cursor: pointer;
                    font-size: 13px;
                    font-weight: 600;
                    transition: all 0.2s;
                }

                .shield-btn-primary {
                    background: #667eea;
                    color: white;
                }

                .shield-btn-primary:hover {
                    background: #5568d3;
                }

                .shield-btn-secondary {
                    background: #2d3748;
                    color: white;
                }

                .shield-btn-secondary:hover {
                    background: #1a202c;
                }

                .toast {
                    position: fixed;
                    top: 20px;
                    left: 50%;
                    transform: translateX(-50%) translateY(-100px);
                    background: #16213e;
                    color: white;
                    padding: 12px 24px;
                    border-radius: 8px;
                    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
                    z-index: 1000000;
                    opacity: 0;
                    transition: all 0.4s ease;
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                    font-size: 14px;
                }

                .toast.visible {
                    transform: translateX(-50%) translateY(0);
                    opacity: 1;
                }

                .toast.success { border-left: 4px solid #2ecc71; }
                .toast.warning { border-left: 4px solid #f39c12; }
                .toast.error { border-left: 4px solid #e74c3c; }
                .toast.info { border-left: 4px solid #3498db; }
            `;
            document.head.appendChild(style);
        }

        createFloatingButton() {
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', () => this.createFloatingButton());
                return;
            }

            const btn = document.createElement('button');
            btn.id = 'qwen-shield-btn';
            btn.innerHTML = '🛡️<span class="badge">0</span>';
            btn.onclick = () => this.togglePanel();
            document.body.appendChild(btn);
        }

        createRecoveryPanel() {
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', () => this.createRecoveryPanel());
                return;
            }

            const panel = document.createElement('div');
            panel.id = 'qwen-shield-panel';
            panel.innerHTML = `
                <div class="shield-header">
                    <h2>🛡️ Qwen Shield</h2>
                    <button class="shield-close">×</button>
                </div>
                <div class="shield-stats">
                    <div class="stat-item">
                        <div class="stat-value" id="stat-saved">0</div>
                        <div class="stat-label">SAVED</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value" id="stat-filtered">0</div>
                        <div class="stat-label">FILTERED</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value" id="stat-intercepted">0</div>
                        <div class="stat-label">INTERCEPTED</div>
                    </div>
                </div>
                <div class="shield-content" id="shield-content">
                    <p style="text-align: center; color: #888; margin-top: 50px;">No filtered content yet</p>
                </div>
                <div class="shield-actions">
                    <button class="shield-btn shield-btn-primary" id="export-btn">Export All</button>
                    <button class="shield-btn shield-btn-secondary" id="clear-btn">Clear</button>
                </div>
            `;

            document.body.appendChild(panel);

            panel.querySelector('.shield-close').onclick = () => this.togglePanel();
            panel.querySelector('#export-btn').onclick = () => this.exportData();
            panel.querySelector('#clear-btn').onclick = () => this.clearData();
        }

        togglePanel() {
            this.panelVisible = !this.panelVisible;
            const panel = document.getElementById('qwen-shield-panel');
            if (this.panelVisible) {
                panel.classList.add('visible');
                this.refreshContent();
            } else {
                panel.classList.remove('visible');
            }
        }

        async refreshContent() {
            const filtered = await shieldDB.getAllFiltered();
            const content = document.getElementById('shield-content');

            if (filtered.length === 0) {
                content.innerHTML = '<p style="text-align: center; color: #888; margin-top: 50px;">No filtered content yet</p>';
                return;
            }

            content.innerHTML = filtered.reverse().map(item => `
                <div class="filtered-item">
                    <div class="filtered-time">${new Date(item.timestamp).toLocaleString()}</div>
                    <div class="filtered-content">${this.escapeHtml(item.originalContent)}</div>
                    ${item.reason ? `<div style="font-size: 11px; color: #ff4757; margin-top: 8px;">Reason: ${item.reason}</div>` : ''}
                </div>
            `).join('');
        }

        updateStats(type) {
            this.stats[type]++;
            const total = this.stats.filtered + this.stats.intercepted;

            document.querySelector('#qwen-shield-btn .badge').textContent = total;

            if (document.getElementById(`stat-${type}`)) {
                document.getElementById(`stat-${type}`).textContent = this.stats[type];
            }
        }

        showToast(message, type = 'info') {
            const toast = document.createElement('div');
            toast.className = `toast ${type}`;
            toast.textContent = message;
            document.body.appendChild(toast);

            setTimeout(() => toast.classList.add('visible'), 10);

            setTimeout(() => {
                toast.classList.remove('visible');
                setTimeout(() => toast.remove(), 400);
            }, 3000);
        }

        async exportData() {
            const filtered = await shieldDB.getAllFiltered();
            const data = {
                exportDate: new Date().toISOString(),
                version: '2.0.0',
                filtered: filtered
            };

            const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `qwen-shield-export-${Date.now()}.json`;
            a.click();
            URL.revokeObjectURL(url);

            this.showToast('Data exported successfully!', 'success');
        }

        async clearData() {
            if (!confirm('Clear all filtered content records?')) return;

            const transaction = shieldDB.db.transaction(['filtered'], 'readwrite');
            const store = transaction.objectStore('filtered');
            store.clear();

            this.stats.filtered = 0;
            this.stats.intercepted = 0;
            this.updateStats('saved'); // Just to trigger UI update
            this.refreshContent();
            this.showToast('Data cleared', 'info');
        }

        escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
    }

    // ==================== NETWORK INTERCEPTOR ====================
    class NetworkInterceptor {
        constructor(ui) {
            this.ui = ui;
            this.init();
        }

        init() {
            this.interceptFetch();
            this.interceptWebSocket();
            this.interceptXHR();
        }

        interceptFetch() {
            const pageGlobal = (typeof unsafeWindow !== 'undefined') ? unsafeWindow : window;
            const originalFetch = pageGlobal.fetch;
            const self = this;

            pageGlobal.fetch = async function(...args) {
                const url = (typeof args[0] === 'string') ? args[0] : args[0]?.url;

                // Target Qwen/DashScope API endpoints
                if (!url || !/(dashscope|qwen|tongyi|aliyun).*\/(chat|completion|generation|conversation|message)/i.test(url)) {
                    return originalFetch.call(pageGlobal, ...args);
                }

                const response = await originalFetch.call(pageGlobal, ...args);
                const contentType = response.headers.get('content-type') || '';

                // Handle SSE streaming
                if (contentType.includes('text/event-stream') || contentType.includes('stream')) {
                    return self.handleSSEResponse(response, args);
                }

                // Handle JSON responses
                if (contentType.includes('application/json')) {
                    return self.handleJSONResponse(response);
                }

                return response;
            };
        }

        async handleSSEResponse(originalResponse, requestArgs) {
            let currentMessageId = null;
            let accumulatedContent = "";
            let wasFiltered = false;

            const stream = new ReadableStream({
                async start(controller) {
                    const reader = originalResponse.body.getReader();
                    const decoder = new TextDecoder();
                    const encoder = new TextEncoder();

                    try {
                        while (true) {
                            const { done, value } = await reader.read();
                            if (done) {
                                if (currentMessageId && accumulatedContent) {
                                    await shieldDB.saveMessage(currentMessageId, accumulatedContent, {
                                        filtered: wasFiltered,
                                        timestamp: Date.now()
                                    });
                                    ui.updateStats('saved');
                                }
                                controller.close();
                                break;
                            }

                            const chunk = decoder.decode(value, { stream: true });
                            const lines = chunk.split('\n');
                            const processedLines = [];

                            for (const line of lines) {
                                if (line.startsWith('data: ') && line !== 'data: [DONE]') {
                                    let jsonStr = line.substring(6).trim();

                                    try {
                                        let data = JSON.parse(jsonStr);

                                        // Extract message ID
                                        if (!currentMessageId) {
                                            currentMessageId = data.id || data.message_id || data.request_id ||
                                                             data.output?.request_id || crypto.randomUUID();
                                        }

                                        // Check for filtering/moderation
                                        const filterDetected = await this.detectFiltering(data);
                                        if (filterDetected) {
                                            wasFiltered = true;
                                            ui.updateStats('intercepted');
                                            ui.showToast('🛡️ Content filtered - saved!', 'warning');

                                            await shieldDB.saveFiltered(
                                                currentMessageId,
                                                accumulatedContent,
                                                '',
                                                filterDetected.reason
                                            );
                                        }

                                        // Extract content
                                        const content = this.extractContent(data);
                                        if (content) {
                                            accumulatedContent += content;
                                        }

                                        jsonStr = JSON.stringify(data);
                                    } catch (e) {
                                        console.error('[Qwen Shield] Parse error:', e);
                                    }

                                    processedLines.push('data: ' + jsonStr);
                                } else {
                                    processedLines.push(line);
                                }
                            }

                            controller.enqueue(encoder.encode(processedLines.join('\n')));
                        }
                    } catch (error) {
                        console.error('[Qwen Shield] Stream error:', error);
                        controller.error(error);
                    }
                }.bind(this)
            });

            return new Response(stream, {
                headers: originalResponse.headers,
                status: originalResponse.status,
                statusText: originalResponse.statusText
            });
        }

        async handleJSONResponse(originalResponse) {
            const text = await originalResponse.text();
            let data;

            try {
                data = JSON.parse(text);

                const filterDetected = await this.detectFiltering(data);
                if (filterDetected) {
                    this.ui.updateStats('intercepted');
                    this.ui.showToast('🛡️ Response filtered - saved!', 'warning');

                    const content = this.extractContent(data);
                    await shieldDB.saveFiltered(
                        data.id || crypto.randomUUID(),
                        content,
                        '',
                        filterDetected.reason
                    );
                }
            } catch (e) {
                console.error('[Qwen Shield] JSON parse error:', e);
            }

            return new Response(text, {
                headers: originalResponse.headers,
                status: originalResponse.status,
                statusText: originalResponse.statusText
            });
        }

        async detectFiltering(data) {
            const flags = [
                'blocked', 'filtered', 'censored', 'moderated',
                'is_blocked', 'is_filtered', 'is_censored', 'is_moderated',
                'content_filtered', 'safety_check', 'policy_violation'
            ];

            // Check direct flags
            for (const flag of flags) {
                if (data[flag] === true) {
                    data[flag] = false; // Unblock
                    return { detected: true, reason: flag };
                }
            }

            // Check nested objects
            if (data.moderation_response || data.moderation_result || data.safety_result) {
                const mod = data.moderation_response || data.moderation_result || data.safety_result;
                for (const flag of flags) {
                    if (mod[flag] === true) {
                        mod[flag] = false;
                        return { detected: true, reason: `moderation.${flag}` };
                    }
                }
            }

            // Check for finish_reason indicating filtering
            if (data.choices && data.choices[0]) {
                const finishReason = data.choices[0].finish_reason;
                if (finishReason && ['content_filter', 'safety', 'policy_violation'].includes(finishReason)) {
                    return { detected: true, reason: `finish_reason: ${finishReason}` };
                }
            }

            // Check output structure (DashScope format)
            if (data.output && data.output.finish_reason) {
                const finishReason = data.output.finish_reason;
                if (['sensitive', 'stop'].includes(finishReason) && data.output.text?.length < 10) {
                    return { detected: true, reason: `output.finish_reason: ${finishReason}` };
                }
            }

            return null;
        }

        extractContent(data) {
            // OpenAI format
            if (data.choices && data.choices[0]) {
                const choice = data.choices[0];
                if (choice.delta && choice.delta.content) return choice.delta.content;
                if (choice.message && choice.message.content) return choice.message.content;
                if (choice.text) return choice.text;
            }

            // DashScope format
            if (data.output) {
                if (data.output.text) return data.output.text;
                if (data.output.content) return data.output.content;
            }

            // Direct fields
            if (data.content) return data.content;
            if (data.text) return data.text;
            if (data.delta) return data.delta;
            if (data.message && data.message.content) return data.message.content;

            return '';
        }

        interceptWebSocket() {
            const pageGlobal = (typeof unsafeWindow !== 'undefined') ? unsafeWindow : window;
            const originalWebSocket = pageGlobal.WebSocket;
            const self = this;

            pageGlobal.WebSocket = function(...args) {
                const ws = new originalWebSocket(...args);

                const originalOnMessage = ws.onmessage;
                ws.onmessage = function(event) {
                    try {
                        const data = JSON.parse(event.data);

                        self.detectFiltering(data).then(filterDetected => {
                            if (filterDetected) {
                                self.ui.updateStats('intercepted');
                                self.ui.showToast('🛡️ WebSocket filtered - saved!', 'warning');

                                const content = self.extractContent(data);
                                shieldDB.saveFiltered(
                                    data.id || crypto.randomUUID(),
                                    content,
                                    '',
                                    `WebSocket: ${filterDetected.reason}`
                                );
                            }
                        });
                    } catch (e) {
                        // Not JSON, ignore
                    }

                    if (originalOnMessage) {
                        return originalOnMessage.apply(this, arguments);
                    }
                };

                return ws;
            };
        }

        interceptXHR() {
            const pageGlobal = (typeof unsafeWindow !== 'undefined') ? unsafeWindow : window;
            const originalOpen = pageGlobal.XMLHttpRequest.prototype.open;
            const originalSend = pageGlobal.XMLHttpRequest.prototype.send;
            const self = this;

            pageGlobal.XMLHttpRequest.prototype.open = function(method, url, ...rest) {
                this._qwenShieldURL = url;
                return originalOpen.apply(this, [method, url, ...rest]);
            };

            pageGlobal.XMLHttpRequest.prototype.send = function(...args) {
                if (this._qwenShieldURL && /(dashscope|qwen|tongyi).*\/(chat|completion)/i.test(this._qwenShieldURL)) {
                    this.addEventListener('load', function() {
                        try {
                            const data = JSON.parse(this.responseText);
                            self.detectFiltering(data).then(filterDetected => {
                                if (filterDetected) {
                                    self.ui.updateStats('intercepted');
                                    const content = self.extractContent(data);
                                    shieldDB.saveFiltered(
                                        data.id || crypto.randomUUID(),
                                        content,
                                        '',
                                        `XHR: ${filterDetected.reason}`
                                    );
                                }
                            });
                        } catch (e) {
                            // Not JSON
                        }
                    });
                }
                return originalSend.apply(this, args);
            };
        }
    }

    // ==================== DOM OBSERVER ====================
    class DOMObserver {
        constructor(ui) {
            this.ui = ui;
            this.messageCache = new Map();
            this.init();
        }

        init() {
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', () => this.startObserving());
            } else {
                this.startObserving();
            }
        }

        startObserving() {
            const observer = new MutationObserver((mutations) => {
                for (const mutation of mutations) {
                    // Detect removed nodes (deleted messages)
                    for (const node of mutation.removedNodes) {
                        if (node.nodeType === 1) { // Element node
                            this.checkForDeletedMessage(node);
                        }
                    }

                    // Detect added nodes (new messages)
                    for (const node of mutation.addedNodes) {
                        if (node.nodeType === 1) {
                            this.cacheMessage(node);
                        }
                    }
                }
            });

            observer.observe(document.body, {
                childList: true,
                subtree: true,
                attributes: true,
                attributeFilter: ['style', 'class']
            });
        }

        cacheMessage(node) {
            // Cache message content from DOM
            // This helps detect when content is modified/removed
            const textContent = node.textContent?.trim();
            if (textContent && textContent.length > 20) {
                const hash = this.simpleHash(textContent);
                this.messageCache.set(hash, {
                    content: textContent,
                    timestamp: Date.now(),
                    node: node
                });
            }
        }

        async checkForDeletedMessage(node) {
            const textContent = node.textContent?.trim();
            if (!textContent || textContent.length < 20) return;

            const hash = this.simpleHash(textContent);
            if (this.messageCache.has(hash)) {
                // Message was cached and now removed
                const cached = this.messageCache.get(hash);

                this.ui.updateStats('filtered');
                this.ui.showToast('🛡️ Message removed from DOM - recovered!', 'warning');

                await shieldDB.saveFiltered(
                    hash,
                    cached.content,
                    '',
                    'DOM removal detected'
                );

                this.messageCache.delete(hash);
            }
        }

        simpleHash(str) {
            let hash = 0;
            for (let i = 0; i < str.length; i++) {
                const char = str.charCodeAt(i);
                hash = ((hash << 5) - hash) + char;
                hash = hash & hash;
            }
            return hash.toString(36);
        }
    }

    // ==================== INITIALIZATION ====================
    console.log('[Qwen Shield] Initializing multi-layered protection...');

    const ui = new ShieldUI();
    const networkInterceptor = new NetworkInterceptor(ui);
    const domObserver = new DOMObserver(ui);

    // Show activation toast
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            ui.showToast('🛡️ Qwen Shield Active - Multi-layer protection enabled', 'success');
        });
    } else {
        ui.showToast('🛡️ Qwen Shield Active - Multi-layer protection enabled', 'success');
    }

    console.log('[Qwen Shield] All systems operational ✓');
})();
