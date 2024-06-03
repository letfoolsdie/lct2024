document.getElementById('searchButton').addEventListener('click', function() {
    var query = document.getElementById('searchBox').value;
    var endpoint = 'http://127.0.0.1:8000/search?query=' + encodeURIComponent(query);

    fetch(endpoint)
        .then(response => response.json())
        .then(data => {
            var resultsContainer = document.getElementById('results');
            resultsContainer.innerHTML = ''; // Clear previous results
            data.forEach(video => {
                var videoFrame = document.createElement('iframe');
                videoFrame.src = video.link;
                videoFrame.allow = 'accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture';
                videoFrame.allowFullscreen = true;
                
                var description = document.createElement('p');
                description.textContent = video.description;
                
                var videoContainer = document.createElement('div');
                videoContainer.appendChild(videoFrame);
                videoContainer.appendChild(description);
                resultsContainer.appendChild(videoContainer);
            });
        })
        .catch(error => {
            console.error('Error fetching the videos:', error);
            alert('Failed to fetch videos. Please try again later.');
        });
});
