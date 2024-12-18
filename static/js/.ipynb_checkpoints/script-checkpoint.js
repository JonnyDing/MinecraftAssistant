document.addEventListener('DOMContentLoaded', () => {
    const sendButton = document.getElementById('send-btn');
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const container = document.getElementById("item-container");
     console.log("开始测试分组数据...");

    // 测试获取分组数据
    fetch("/test_items")
        .then(response => response.json())
        .then(data => {
            console.log("分组数据获取成功：", data);
        })
        .catch(error => {
            console.error("获取分组数据出错：", error);
        });
     // 异步获取分类数据
    fetch("/get_items")
        .then(response => response.json())
        .then(data => {
            for (let category in data) {
                // 创建分类按钮
                const categoryDiv = document.createElement("div");
                categoryDiv.className = "item-category";

                const button = document.createElement("button");
                button.className = "category-btn";
                button.textContent = category;

                // 创建物品列表
                const ul = document.createElement("ul");
                ul.className = "item-list";
                ul.style.display = "none"; // 初始隐藏

                data[category].forEach(item => {
                    const li = document.createElement("li");
                    li.textContent = item;
                    ul.appendChild(li);
                });

                // 点击按钮展开/折叠列表
                button.addEventListener("click", () => {
                    ul.style.display = ul.style.display === "none" ? "block" : "none";
                });

                categoryDiv.appendChild(button);
                categoryDiv.appendChild(ul);
                container.appendChild(categoryDiv);
            }
        })
        .catch(error => {
            console.error("获取数据出错:", error);
            container.innerHTML = "<p>无法加载物品数据，请稍后重试。</p>";
        });
    // 函数：追加用户或 NPC 消息
    function appendMessage(message, sender) {
        const messageContainer = document.createElement('div');
        messageContainer.classList.add('message-container', sender === "user" ? "user" : "npc");

        // 用户或 NPC 头像
        const avatar = document.createElement('img');
        avatar.src = sender === "user" ? "static/images/steve.jpg" : "static/images/npc.jpg";
        avatar.alt = sender === "user" ? "用户" : "NPC";
        avatar.classList.add('avatar');

        // 消息文本内容
        const messageElement = document.createElement('div');
        messageElement.classList.add('message');
        messageElement.textContent = message;

        // 添加到消息容器
        messageContainer.appendChild(avatar);
        messageContainer.appendChild(messageElement);
        chatBox.appendChild(messageContainer);
        chatBox.scrollTop = chatBox.scrollHeight; // 滚动到底部
    }

    // 函数：显示 NPC 输入中的指示器
    function showTypingIndicator() {
        const typingIndicator = document.createElement('p');
        typingIndicator.textContent = "NPC 正在输入...";
        typingIndicator.classList.add("npc-message", "typing");
        chatBox.appendChild(typingIndicator);
        chatBox.scrollTop = chatBox.scrollHeight;
        return typingIndicator;
    }
    
    // 函数：发送消息
    function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return; // 避免发送空消息

        appendMessage(message, "user"); // 显示用户消息
        userInput.value = ''; // 清空输入框

        const typingIndicator = showTypingIndicator(); // 显示 "正在输入" 指示

        // 发送请求到后端
        fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            typingIndicator.remove(); // 移除指示器
            if (data.response) {
                appendMessage(data.response, "npc");
            } else {
                appendMessage("NPC 无法生成回复，请稍后重试！", "npc");
            }
        })
        .catch(() => {
            typingIndicator.remove();
            appendMessage("网络错误，请稍后重试。", "npc");
        });
    }

    // 事件监听：点击发送按钮
    sendButton.addEventListener('click', sendMessage);

    // 事件监听：回车发送消息（Shift + Enter 换行）
    userInput.addEventListener('keydown', (event) => {
        if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            sendMessage();
        }
    });

    // 函数：折叠/展开分类列表
    function toggleCategoryList() {
        const itemList = this.nextElementSibling;
        itemList.style.display = (itemList.style.display === 'block') ? 'none' : 'block';
    }

    // 初始化分类按钮的点击事件
    const categoryButtons = document.querySelectorAll('.category-btn');
    categoryButtons.forEach(button => {
        button.addEventListener('click', toggleCategoryList);
    });
});
