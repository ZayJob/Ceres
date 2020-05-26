const app = {
    pages: [],
    show: new Event('show'),
    init: function(){
        app.pages = document.querySelectorAll('.page');
        app.pages.forEach((pg)=>{
            pg.addEventListener('show', app.pageShown);
        })
        
        document.querySelectorAll('.nav-link').forEach((link)=>{
            link.addEventListener('click', app.nav);
        })
        history.replaceState({}, '', '#home');
        window.addEventListener('popstate', app.poppin);

        document.querySelector('.lgt').addEventListener('click', logout)
        document.querySelector('.prf').addEventListener('click', profile)
    },
    nav: function(ev){
        ev.preventDefault();
        let currentPage = ev.target.getAttribute('data-target');
        document.querySelector('.active').classList.remove('active');
        document.getElementById(currentPage).classList.add('active');
        history.pushState({}, currentPage, `#${currentPage}`);
        document.getElementById(currentPage).dispatchEvent(app.show);
    },
    pageShown: function(ev){
        ev.preventDefault();
        document.querySelector('.active').innerHTML = "<div class='loader'></div>";

        setTimeout( function(){
            let currentPage = document.querySelector('.active').getAttribute('id');

            fetch(`/render_page?page=${currentPage}`, 
                { 
                method: "GET", 
                headers:{"content-type":"application/x-www-form-urlencoded"} 
            })
            .then( response => {
                if (response.status !== 200) {
                    
                    return Promise.reject(); 
                }
                return response.text()
            })
            .then( i => {
                document.querySelector('.active').innerHTML = i;
                if (`${currentPage}` == 'search_food') {
                    const form_search_food = document.getElementById('search_food_form')
                    form_search_food.addEventListener('submit', search_food)
                } else if (`${currentPage}` == 'login') {
                    const form_login = document.getElementById('login_form')
                    form_login.addEventListener('submit', login)
                } else if (`${currentPage}` == 'calculator') {
                    const form_calculator = document.getElementById('calculator_form')
                    form_calculator.addEventListener('submit', calculator)
                } else if (`${currentPage}` == 'signup') {
                    const form_signup = document.getElementById('signup_form')
                    form_signup.addEventListener('submit', signup)
                }
            })
            .catch(() => console.log('ошибка'));  
        }, 1500 );
    },
    poppin: function(ev){
        console.log(location.hash, 'popstate event');
        let hash = location.hash.replace('#' ,'');
        document.querySelector('.active').classList.remove('active');
        document.getElementById(hash).classList.add('active');
        console.log(hash)
        document.getElementById(hash).dispatchEvent(app.show);
    }
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function login(e) {
    e.preventDefault();
    fetch(`/login`, 
    { 
        method: "POST",
        body: "username=" + document.getElementById("username").value + "&password=" + document.getElementById("password").value,
        headers: {"content-type": "application/x-www-form-urlencoded", "X-CSRFToken": getCookie('csrftoken') },
    })
    .then( response => {
        if (response.status !== 200) {
            
            return Promise.reject(); 
        }
        return response.text()
    })
    .then( i => {
        if (i == "no") {
            alert("Not successfully")
        } else {
            document.querySelector('.active').innerHTML = i;
            document.getElementById('login_link').classList.add('deactivate');
            document.getElementById('signup_link').classList.add('deactivate');
            document.getElementById('logout_link').classList.remove('deactivate');
            alert("Success")
        }
    })
    .catch(() => console.log('ошибка'));
};

function search_food(e) {
    e.preventDefault();
    fetch(`/search_food`, 
    { 
        method: "POST",
        body: "data=" + document.getElementById("data").value,
        headers: {"content-type": "application/x-www-form-urlencoded", "X-CSRFToken": getCookie('csrftoken') },
    })
    .then( response => {
        if (response.status !== 200) {
            
            return Promise.reject(); 
        }
        return response.text()
    })
    .then( i => {
        document.querySelector('.active').innerHTML = i;
        const form_search_food = document.getElementById('search_food_form')
        form_search_food.addEventListener('submit', search_food)
    })
    .catch(() => console.log('ошибка'));
};

function calculator(e) {
    e.preventDefault();
    fetch(`/calculator`, 
    { 
        method: "POST",
        body: 'age=' + document.getElementById("age").value + 
        '&female=' + document.getElementById("female").value + 
        '&male=' + document.getElementById("male").value + 
        '&weight=' + document.getElementById("weight").value + 
        '&height=' + document.getElementById("height").value + 
        '&activ=' + document.getElementById("activ").value,
        headers: {"content-type": "application/x-www-form-urlencoded", "X-CSRFToken": getCookie('csrftoken') },
    })
    .then( response => {
        if (response.status !== 200) {
            
            return Promise.reject(); 
        }
        return response.text()
    })
    .then( i => {
        document.querySelector('.active').innerHTML = i;

        var ctx = document.getElementById('myChart').getContext('2d');
        var carbohydrate = document.getElementById('carbohydrate');
        var fat = document.getElementById('fat');
        var protein = document.getElementById('protein');


        if (carbohydrate.innerText.split(" ").length == 1)
            carbohydrate = 0
        else
            carbohydrate = Number(carbohydrate.innerText.split(" ")[0])

        if (fat.innerText.split(" ").length == 1)
            fat = 0
        else
            fat = Number(fat.innerText.split(" ")[0])

        if (protein.innerText.split(" ").length == 1)
            protein = 0
        else
            protein = Number(protein.innerText.split(" ")[0])

        var myChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Carbohydrate', 'Fat', 'Protein'],
                datasets: [{
                    data: [carbohydrate, fat, protein],
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                    ],
                    borderWidth: 1
                }]
            },
        });

        const form_calculator = document.getElementById('calculator_form')
        form_calculator.addEventListener('submit', calculator)
    })
    .catch(() => console.log('ошибка'));
};

function logout(e) {
    e.preventDefault();
    fetch(`/logout`, 
    { 
        method: "GET", 
        headers:{"content-type":"application/x-www-form-urlencoded"} 
    })
    .then( response => {
        if (response.status !== 200) {
            
            return Promise.reject(); 
        }
        return response.text()
    })
    .then( i => {
        document.getElementById('login_link').classList.remove('deactivate');
        document.getElementById('signup_link').classList.remove('deactivate');
        document.getElementById('logout_link').classList.add('deactivate');
        document.querySelector('.active').classList.remove('active');
        document.getElementById("home").classList.add('active');
        document.querySelector('.active').innerHTML = i;
    })
    .catch(() => console.log('ошибка')); 
};

function profile(e) {
    e.preventDefault();
    fetch(`/profile`, 
    { 
        method: "GET", 
        headers:{"content-type":"application/x-www-form-urlencoded"} 
    })
    .then( response => {
        if (response.status !== 200) {
            
            return Promise.reject(); 
        }
        return response.text()
    })
    .then( i => {
        if (i == "no") {
            alert("Auth pls")
        } else {
            document.getElementById('login_link').classList.add('deactivate');
            document.getElementById('signup_link').classList.add('deactivate');
            document.getElementById('logout_link').classList.remove('deactivate');
            document.querySelector('.active').innerHTML = i;
        }
    })
    .catch(() => console.log('ошибка')); 
};

function signup(e) {
    e.preventDefault();
    fetch(`/signup`, 
    { 
        method: "POST",
        body: "first_name=" + document.getElementById("first_name").value + 
        "&last_name=" + document.getElementById("last_name").value + 
        "&username=" + document.getElementById("username").value + 
        "&email=" + document.getElementById("email").value + 
        "&password1=" + document.getElementById("password1").value + 
        "&phone=" + document.getElementById("phone").value + 
        "&url=" + document.getElementById("url").value + 
        "&company=" + document.getElementById("company").value + 
        "&address=" + document.getElementById("address").value,
        headers: {"content-type": "application/x-www-form-urlencoded", "X-CSRFToken": getCookie('csrftoken') },
    })
    .then( response => {
        if (response.status !== 200) {
            
            return Promise.reject(); 
        }
        return response.text()
    })
    .then( i => {
        if (i == "no") {
            alert("Not successfully")
        } else {     
            document.querySelector('.active').innerHTML = i;
            const form_signup = document.getElementById('signup_form')
            form_signup.addEventListener('submit', signup)
        }
    })
    .catch(() => console.log('ошибка'));
};

document.addEventListener('DOMContentLoaded', app.init);