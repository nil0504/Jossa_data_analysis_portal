let backgroundOption = true;
let backgroundInterval;
let landingPage = document.getElementById("landing-page2");

//Get Array of Images
let imgsArray = ["Study4.jpg","Study1.jpg","Study2.jpg","Study3.jpg"];

//Function To Randomize Imgs
function randomizeImgs() {
    if (backgroundOption === true) {
        backgroundInterval = setInterval(() => {
            //Get Random Number
            let randomNumber = Math.floor(Math.random() * imgsArray.length);
            //Change Background Image url
            landingPage.style.backgroundImage =
                'url("/static/images/' + imgsArray[randomNumber] + '")';
        }, 1500);
    }
}
randomizeImgs();
