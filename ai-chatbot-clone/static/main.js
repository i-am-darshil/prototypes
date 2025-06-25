let token = null;

document.getElementById('loginForm').addEventListener('submit', async function (e) {
  e.preventDefault();
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;

  const res = await fetch('/api/login', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({username, password})
  });

  const data = await res.json();
  if (res.ok) {
    token = data.token;
    conv_history = data.conv_history;
    credits = data.credits;
    document.getElementById('user').innerText = username;
    document.getElementById('loginForm').style.display = 'none';
    document.getElementById('chatContainer').style.display = 'block';
    document.getElementById('credits').innerText = credits;

    const chatBox = document.getElementById('chatBox');
    const randomNumber = Math.random();
    for (let i = 0; i < conv_history.length; i++) {
      const { user_message, bot_response } = conv_history[i];
      chatBox.innerHTML += `<div style="margin:4px;"><b>You:</b> ${user_message}</div><div style="background:rgb(223, 223, 223); padding: 10px; margin-top: 5px; border-radius: 4px; font-family: monospace;"><br/><b>Bot:</b> <github-md id="streaming-${randomNumber}">${bot_response}</github-md></div>`;
      renderMarkdown();
    }
    chatBox.scrollTop = chatBox.scrollHeight;
  } else {
    alert(data.message);
  }
  document.getElementById('signup').style.display = 'none';
});

async function sendPrompt() {
  const prompt = document.getElementById('prompt').value;
  const chatBox = document.getElementById('chatBox');
  const randomNumber = Math.random();
  chatBox.innerHTML += `<div style="margin:4px;"><b>You:</b> ${prompt}</div><div style="background:rgb(223, 223, 223); padding: 10px; margin-top: 5px; border-radius: 4px; font-family: monospace;"><br/><b>Bot:</b> <github-md id="streaming-${randomNumber}"></github-md></div>`;
  document.getElementById('prompt').value = '';

  const res = await fetch('/api/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({prompt})
  });

  // console.log(`Response: ${JSON.stringify(res)}`)

  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let botText = '';
  while (true) {
    const { value, done } = await reader.read();
    // console.log(`value: ${value}`);
    if (done) break;
    const chunk = decoder.decode(value);
    botText += chunk;
    // document.getElementById(`streaming-${randomNumber}`).innerHTML = marked.parse(botText);
    document.getElementById(`streaming-${randomNumber}`).innerHTML = botText;
    renderMarkdown();
  }
  chatBox.scrollTop = chatBox.scrollHeight;
  document.getElementById('credits').innerText = parseInt(document.getElementById('credits').innerText) + 1;
}
