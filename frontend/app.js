let recorder, audioBlob;

document.getElementById("record").onclick = async () => {
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  recorder = new MediaRecorder(stream);
  recorder.start();

  recorder.ondataavailable = e => audioBlob = e.data;

  setTimeout(() => recorder.stop(), 5000);
};

document.getElementById("submit").onclick = () => {
  navigator.geolocation.getCurrentPosition(pos => {
    const form = new FormData();
    form.append("audio", audioBlob);
    form.append("lat", pos.coords.latitude);
    form.append("lon", pos.coords.longitude);

    fetch("https://YOUR_RENDER_URL/complaint", {
      method: "POST",
      body: form
    })
    .then(r => r.json())
    .then(() => status.innerText = "Complaint Submitted");
  });
};
