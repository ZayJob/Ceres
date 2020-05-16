var ctx = document.getElementById('myChart').getContext('2d');
var carbohydrate = document.getElementById('carbohydrate');
var fat = document.getElementById('fat');
var protein = document.getElementById('protein');

console.log(carbohydrate.innerText.split(" "))

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