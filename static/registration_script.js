// check atleast one hobby must be selected
function checkbox_hobby() {
    var hobby_1 = document.getElementById('sport').checked;
    var hobby_2 = document.getElementById('music').checked;
    var hobby_3 = document.getElementById('read').checked;
    var hobby_4 = document.getElementById('other').checked;
    var createButton = document.getElementById('submit_button');
    var flag = false;

    if (!hobby_1 && !hobby_2 && !hobby_3 && !hobby_4) {
        createButton.disabled = true;
        createButton.style.opacity = 0.4;
        flag = true;
    } else {
        createButton.disabled = false;
        createButton.style.opacity = 1;
        flag = false;
    }

    if (flag) {
        document.getElementById('hobby_tick').style.color = 'red';
        document.getElementById('hobby_tick').innerHTML = "Please check at least one checkbox for Hobbies";
    } else {
        document.getElementById('hobby_tick').innerHTML = "";
    }
}

// cout address must be minimum 15 word
function countwords() {
    let res = [];
    let str = document.querySelector("#address").value.replace(/[\t\n\r\.\?\!]/gm, " ").split(" ");
    str.map((s) => {
        let trimStr = s.trim();
        if (trimStr.length > 0) {
            res.push(trimStr);
        }
    });

    if (res.length < 10) {
        document.getElementById("short_add").style.color = "red";
        document.getElementById("short_add").innerHTML = "Address should be longer than 10 words";
    } else {
        document.getElementById("short_add").innerHTML = "";
    }
}

//Checks if  password and confirm password are same or not
function validate_password() {
    var pass = document.getElementById('password').value;
    var confirm_pass = document.getElementById('confirm_password').value;
    var createButton = document.getElementById('submit_button');

    if (pass !== confirm_pass) {
      document.getElementById('wrong_pass_alert').style.color = 'red';
      document.getElementById('wrong_pass_alert').innerHTML = 'Password and Confirm Password are different';
      createButton.disabled = true;
      createButton.style.opacity = 0.4;
    } else {
      document.getElementById('wrong_pass_alert').style.color = 'green';
      document.getElementById('wrong_pass_alert').innerHTML = 'Password Matched';
      createButton.disabled = false;
      createButton.style.opacity = 1;
    }
  }