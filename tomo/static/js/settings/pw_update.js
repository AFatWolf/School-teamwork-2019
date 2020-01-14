/* this is the password input field */
var password = target.previousElementSibling;
( 'password' == password.getAttribute('type') ) ? password.setAttribute('type', 'text') : 
password.setAttribute('type', 'password');
target.textContent = ( 'Hide' == target.textContent ) ? 'Show' : 'Hide';
putCursorAtEnd(password);