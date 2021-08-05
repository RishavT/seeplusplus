// TODO: Replace the following with your app's Firebase project configuration
// For Firebase JavaScript SDK v7.20.0 and later, `measurementId` is an optional field
var firebaseConfig = {
    apiKey: "AIzaSyAjN77HqvuFsLpPfjZiKRlNaEOqB7MAFl4",
    authDomain: "copypp1.firebaseapp.com",
    databaseURL: "https://copypp1.firebaseio.com",
    projectId: "copypp1",
    storageBucket: "copypp1.appspot.com",
    messagingSenderId: "717871322376",
    appId: "1:717871322376:web:40b89404646f4ec2cac8bd"
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);
var db = firebase.database();
const ClipboardKey = '/clipboard';
const Base64Prefix = '__base64_file';
var clipboardRef = db.ref(ClipboardKey);

function b64toFile(value) {
    // TODO Implement this
    return value;
}


function getLatestClipboardValue(callback) {
     clipboardRef.get().then(x => {
         var value = x.val();
         if (value && value !== Base64Prefix && value.startsWith(Base64Prefix)) {
             // Convert from base64
             value = b64toFile(value);
         }
         callback(value);
     });
}

function setLatestClipboardValue(value, callback) {
    // TODO add file handling
    clipboardRef.set(value).then(callback);
}

function pushToClipboard() {
    // Pastes text from the system into the input and then pushes to the
    // firebase clipboard
    var element = document.getElementById("clipboard-text");
    element.click();
    navigator.clipboard.readText().then(text => {
        if (!text) {
            text = element.value;
        }
        if (text) {
            setLatestClipboardValue(text, () => {
                element.value = text;
            });
        }
    });
}

function getFromClipboard() {
    // Gets the latest value from the firebase clipboard and copies to
    // clipboard
    var element = document.getElementById("clipboard-text");
    getLatestClipboardValue(text => {
        if (text) {
            element.value = text;
            navigator.clipboard.writeText(text).then(console.log);
        }
    });
}   
