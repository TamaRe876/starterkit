
    document.addEventListener('DOMContentLoaded', function() {
        let posts = {{ posts|json_script:"posts" }};
        
        posts.forEach(post => {
            const waveSurfer = WaveSurfer.create({
                container: `#waveform-${post.id}`,
                waveColor: 'gray',
                progressColor: 'blue',
                height: 64,
                responsive: true
            });
            waveSurfer.load(post.song.url);

            document.querySelector(`#play-btn-${post.id}`).addEventListener('click', function() {
                waveSurfer.playPause();
                togglePlay(post.id);
            });

            document.querySelector(`#pause-btn-${post.id}`).addEventListener('click', function() {
                waveSurfer.playPause();
                togglePlay(post.id);
            });

            waveSurfer.on('play', function() {
                document.querySelector(`#play-btn-${post.id}`).classList.add('hidden');
                document.querySelector(`#pause-btn-${post.id}`).classList.remove('hidden');
            });

            waveSurfer.on('pause', function() {
                document.querySelector(`#play-btn-${post.id}`).classList.remove('hidden');
                document.querySelector(`#pause-btn-${post.id}`).classList.add('hidden');
            });
        });
    });

    function togglePlay(id) {
        document.querySelector(`#play-btn-${id}`).classList.toggle('hidden');
        document.querySelector(`#pause-btn-${id}`).classList.toggle('hidden');
    }

