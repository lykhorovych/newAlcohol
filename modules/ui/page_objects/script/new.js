// let a = name ? true : false - тернарний оператор

function createNumbers () {
    document.querySelector('#result').value = ''
    const num = Number(document.querySelector('select').value);
    let num1 = Math.floor(Math.random() * 10 ** num);
    let num2 = Math.floor(Math.random() * 10 ** num);
    if (num2 > num1) {
        let temp = num1;
        num1 = num2;
        num2 = temp;
    }
    const result = String(num1 + num2).length;
    console.log(result)
    for (i=0; i < result; i++) {
        console.log(i)
        const f_num = document.createElement('input');
        f_num.setAttribute('class', 'result_fields');
        f_num.setAttribute('maxlength', '1');
        f_num.setAttribute('required', 'required');

        document.querySelector('#result_numbers').appendChild(f_num);
    }
    document.querySelector('.input-hidden').value = `${num1} + ${num2}`;
    document.querySelector('#expression').value = `${num1} + ${num2} =`;
}

document.addEventListener('DOMContentLoaded', createNumbers
);

document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('form').onsubmit = () =>  {
        //alert('submit');
        let count = localStorage.getItem('index');
        let rs = document.querySelectorAll('.result_fields');
        let numb = '';
        for (let el of rs) {
            numb += el.value;
        }
        document.querySelector('#result').value = numb
        const result = Number(document.querySelector('#result').value);
        const expression = document.querySelector('.input-hidden').value;
        let numbers = expression.split('+');
        let num1 = Number(numbers[0]);
        let num2 = Number(numbers[1]);
        console.log(result, expression, num1, num2)
        if (result === num1+num2) {
            //alert('Вірно');
            const tableRow = `<th scope='row'>${count}</th><td>${expression} = X</td><td>${result}</td><td id='td-result__true'>Вірно</td><td>@mdo</td>`;
            const tr = document.createElement('tr');
            tr.innerHTML = tableRow;
            const tableBody = document.querySelector('tbody');
            tableBody.prepend(tr)
            count ++;
            localStorage.setItem('index', count)
            let rs = document.querySelectorAll('.result_fields');
            for (let el of rs) {
                el.remove();
            }
            createNumbers();
        } else {
            //alert('Не вірно');
            const tableRow = `<th scope='row'>${count}</th><td>${expression} = X</td><td>${result}</td><td id='td-result__false'>Не вірно</td><td>@mdo</td>`;
            const tr = document.createElement('tr');
            tr.innerHTML = tableRow;
            const tableBody = document.querySelector('tbody');
            tableBody.prepend(tr)
            count ++;
            localStorage.setItem('index', count);
            let rs = document.querySelectorAll('.result_fields');
            for (let el of rs) {
                el.remove();
            }
            createNumbers();
        }
        return false;
        }
    }
);

document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#select').onchange = () => {
        createNumbers()}});

document.addEventListener('DOMContentLoaded', () => {
    const inputs = document.querySelectorAll('.result_fields'); 
    for (let el of inputs) {
        if (!el.value) {
            el.focus();
            break;
        }
    }
});


