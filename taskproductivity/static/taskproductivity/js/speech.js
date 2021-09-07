// Code adapted from https://github.com/mdn/web-speech-api/tree/master/speech-color-changer
var SpeechRecognition = SpeechRecognition || webkitSpeechRecognition
var SpeechGrammarList = SpeechGrammarList || webkitSpeechGrammarList
var SpeechRecognitionEvent = SpeechRecognitionEvent || webkitSpeechRecognitionEvent

// Create the SpeechRecognition object. 
var recognition = new SpeechRecognition();
recognition.continuous = false;
// This will need to be the same as the content that is created
recognition.lang = 'en-US';
recognition.interimResults = false;
recognition.maxAlternatives = 1;

// Once the start button has been clicked, start the recognition and reset all the texts.
document.getElementById("btn_start").onclick = function() {
    recognition.start();
    console.log('Ready to receive a color command.');
    const status = document.getElementById("status");
    const comparison = document.getElementById("comparison");
    const score = document.getElementById("score");
    status.textContent = "Status: Please Start Speaking"
    comparison.innerHTML = '';
    score.innerHTML = '';
}

recognition.onresult = function(event) {
    // The SpeechRecognitionEvent results property returns a SpeechRecognitionResultList object
    // The SpeechRecognitionResultList object contains SpeechRecognitionResult objects.
    // It has a getter so it can be accessed like an array
    // The first [0] returns the SpeechRecognitionResult at the last position.
    // Each SpeechRecognitionResult object contains SpeechRecognitionAlternative objects that contain individual results.
    // These also have getters so they can be accessed like arrays.
    // The second [0] returns the SpeechRecognitionAlternative at position 0.
    // We then return the transcript property of the SpeechRecognitionAlternative object
    var spoken = event.results[0][0].transcript;
    const status = document.getElementById("status");
    const sentence = document.getElementById("sentence");
    const score = document.getElementById("score");
    const comparison = document.getElementById("comparison");
    const words = sentence.value.split(" ");
    const lowered_words = sentence.value.toLowerCase().split(" ");
    const spoken_words = spoken.toLowerCase().split(" ");
    const words_len = words.length;
    const spoken_words_len = spoken_words.length;

    // Show what is recognized by the speech to text engine
    status.textContent = 'I heard "' + spoken + '".';
    
    // Scoring logic
    let correct_count = 0;
    let result = document.createElement("h3");
    result.className = "comparison"
    const last_word_pos = words_len - 1

    if (words_len >= spoken_words_len) {
        for (let i = 0; i < spoken_words_len; i++) {
            if (lowered_words[i] == spoken_words[i]) {
                correct_count++;
                if (i < last_word_pos) {
                    const txt = document.createTextNode(words[i] + " ");
                    result.appendChild(txt);
                }
                else{
                    const txt = document.createTextNode(words[i]);
                    result.appendChild(txt);
                }
            }
            // Highlight the words that are incorrect in red
            else {
                const span = document.createElement("span");
                span.className = "wrong";
                if (i < last_word_pos) {
                    const txt = document.createTextNode(words[i] + " ");
                    span.appendChild(txt);
                }
                else{
                    const txt = document.createTextNode(words[i]);
                    span.appendChild(txt);
                }
                result.appendChild(span)
            }
        }
    }
    else {
        let last_index = 0;
        for (let i = 0; i < words_len; i++) {
            if (lowered_words[i] == spoken_words[i]) {
                correct_count++;
                if (i < last_word_pos) {
                    const txt = document.createTextNode(words[i] + " ");
                    result.appendChild(txt);
                }
                else{
                    const txt = document.createTextNode(words[i]);
                    result.appendChild(txt);
                }
            }
            else {
                const span = document.createElement("span");
                span.className = "wrong";
                if (i < last_word_pos) {
                    const txt = document.createTextNode(words[i] + " ");
                    span.appendChild(txt);
                }
                else{
                    const txt = document.createTextNode(words[i]);
                    span.appendChild(txt);
                }
                result.appendChild(span)
            }
            last_index = i;
        }

        // This is the logic to highlight blanks if the returned text is longer than the original text.
        const diff = spoken_words_len - last_index - 1;
        const before_last = diff - 1;
        for (let i = 0; i < diff; i++) {
            const span = document.createElement("span");
            span.className = "wrong";
            const txt = document.createTextNode(" _");
            span.appendChild(txt);
            result.appendChild(span);
        }
    }

    // The logic to add penalty when the recognized text is longer than the original text. 
    if (words_len < spoken_words_len) {
        const diff = spoken_words_len - words_len;
        correct_count -= diff;
    }

    // The scoring logic is the total correct words divided by the word length multiply by 100.
    const total_score = correct_count / words_len * 100;

    score.textContent = "Score: " + Math.round(total_score * 10) / 10;
    console.log(sentence.textContent);
    comparison.appendChild(result);
    console.log('Confidence: ' + event.results[0][0].confidence);
}

recognition.onspeechend = function() {
    recognition.stop();
    const status = document.getElementById("status");
    status.textContent = "Status: Speech ended. Starting recognition"
}

recognition.onnomatch = function(event) {
    const status = document.getElementById("status");
    status.textContent = "Status: I am sorry. I didn't quite get what you said. Please try again?"
}

recognition.onerror = function(event) {
    const status = document.getElementById("status");
    status.textContent = 'Error occurred in recognition: ' + event.error;
}
