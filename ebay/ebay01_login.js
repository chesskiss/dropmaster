var casper = require('casper').create( {
    verbose: true, 
    logLevel: 'debug',
   // userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
});

var email = "cohenshlomi863@gmail.com";
var pass = "Rona7890!"; 

//var sign_in_button = 'a.gh-ug-guest';
var sign_in_button = '#signin-button button';
var user_field_id = 'input#userid';
var continue_button_id = '#signin-continue-btn';
var password_field_id = 'input#pass';
var submit_button_id = '#sgnBt'



// open eBay homepage
casper.start('https://www.ebay.com/', function() {
  this.echo('eBay homepage opened');
});

// click on "Sign in" link
casper.then(function() {
  this.clickLabel('Sign in');
  this.echo('Clicking on "Sign in" link');
});

// wait for login page to load
casper.waitForSelector('#signin-button button', function() {
  this.echo('Login page loaded');
});

// take a screenshot of the login page
casper.then(function() {
  this.capture('ebay_login.png');
  this.echo('Screenshot taken');
});

/*
casper.start('https://www.ebay.com/sellercenter', function() {
//casper.start('https://signin.ebay.com/ws/eBayISAPI.dll?SignIn&ru=https%3A%2F%2Fwww.ebay.com%2Fsellercenter', function() {
    // Wait for the page to load
    


    console.log('Current URL: ' + this.getCurrentUrl());
        console.log('Current title: ' + this.getTitle());
        this.capture('after_login.png');
        var html = this.getPageContent();
    this.download(html, 'signin.html');

    this.waitForSelector(sign_in_button, function() {  
        this.click(sign_in_button);
    });

});

casper.then(function() {
    this.waitForSelector(user_field_id, function() {  
        this.sendKeys(user_field_id, email);
        
    });

});

casper.then(function() {
    this.click(continue_button_id);
});

casper.then(function() {
    this.waitForSelector(password_field_id, function() {  
         this.sendKeys(password_field_id, pass);
    });
 });
 */  

 casper.then(function() {
     //this.click(submit_button_id);
     casper.wait(3000, function() {
         console.log('Current URL: ' + this.getCurrentUrl());
         console.log('Current title: ' + this.getTitle());
         this.capture('after_login.png');
     });
 });
 casper.run();