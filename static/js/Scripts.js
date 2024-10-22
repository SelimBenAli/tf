function check_mat_validation() {
    mail = document.getElementById("email");
    mat = document.getElementById("mat");
    if (mat.value === '') {
        alert('matricule vide');
        return;
    }

    type = '';
    const radios = document.getElementsByName("type");
    for (const radio of radios) {
        if (radio.checked) {
            type = radio.id;
        }
    }

    if (type === '') {
        alert('Choisissez un type');
        return;
    }


    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/personne/existe?matricule=' + mat.value + '&email=' + mail.value + '&type=' + type, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            console.log("ttt", response)

            if (response.status === 'success') {
                console.log("rrr", response)
                if (response.exist === 'true') {
                    if (response.answers === 'false') {
                        next_page(1);
                    } else {
                        alert("Déjà répondu");
                    }
                } else {
                    alert('n\'existe pas');
                }
            }

        }
    }
    xhr.send();

}

function request_question(q) {
    console.log(q)
    alert('Veuillez répondre à la question ' + q[q.length - 1]);
}

function check_answers_1() {
    const questions = ['q1', 'q2', 'q3', 'q4', 'q5', 'q6'];
    let answers = {};

    function getCheckedValue(question) {
        const radios = document.getElementsByName(question);
        for (const radio of radios) {
            if (radio.checked) {
                return radio.id;
            }
        }
        return '';
    }

    for (const question of questions) {
        const answer = getCheckedValue(question);
        if (answer === '') {
            request_question(question);
            return;
        }
        answers[`F1-${questions.indexOf(question) + 1}`] = answer;
    }

    console.log(answers);
    send_answers(1, answers)
}


function check_answers_2() {
    const questions = ['q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8'];
    let answers = {};

    function getCheckedValue(question) {
        const radios = document.getElementsByName(question);
        for (const radio of radios) {
            if (radio.checked) {
                return radio.id;
            }
        }
        return '';
    }

    for (const question of questions) {
        const answer = getCheckedValue(question);
        if (answer === '') {
            request_question(question);
            return;
        }
        answers[`F2-${questions.indexOf(question) + 1}`] = answer;
    }

    console.log(answers);
    send_answers(2, answers)
}

function check_answers_3() {
    const questions = ['q1', 'q2', 'q3', 'q4', 'q5', 'q6'];
    let answers = {};

    function getCheckedValue(question) {
        const radios = document.getElementsByName(question);
        for (const radio of radios) {
            if (radio.checked) {
                return radio.id;
            }
        }
        return '';
    }

    for (const question of questions) {
        const answer = getCheckedValue(question);
        if (answer === '') {
            request_question(question);
            return;
        }
        answers[`F3-${questions.indexOf(question) + 1}`] = answer;
    }

    console.log(answers);
    send_answers(3, answers)
}

function check_answers_4() {
    const questions = ['q1', 'q2', 'q3', 'q4', 'q5', 'q6'];
    let answers = {};

    function getCheckedValue(question) {
        const radios = document.getElementsByName(question);
        for (const radio of radios) {
            if (radio.checked) {
                return radio.id;
            }
        }
        return '';
    }

    for (const question of questions) {
        const answer = getCheckedValue(question);
        if (answer === '') {
            request_question(question);
            return;
        }
        answers[`F4-${questions.indexOf(question) + 1}`] = answer;
    }

    console.log(answers);
    send_answers(4, answers)
}

function check_answers_5() {
    const questions = ['q1', 'q2', 'q3', 'q4', 'q5', 'q6'];
    let answers = {};

    function getCheckedValue(question) {
        const radios = document.getElementsByName(question);
        for (const radio of radios) {
            if (radio.checked) {
                return radio.id;
            }
        }
        return '';
    }

    for (const question of questions) {
        const answer = getCheckedValue(question);
        if (answer === '') {
            request_question(question);
            return;
        }
        answers[`F5-${questions.indexOf(question) + 1}`] = answer;
    }

    console.log(answers);
    send_answers(5, answers)
}

function send_answers(page, answers) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/forms/post-responses', true);
    xhr.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            if (response.status === 'success') {
                console.log("ok")
                if (page < 5) {
                    next_page(page + 1);
                } else {
                    envoyer();
                }
            } else {
                if (response.exist === 'false') {
                    window.location.href = '/'
                }
            }

        }
    }
    xhr.send(JSON.stringify({'reponses': answers, 'page': page}));
}

function envoyer() {
    window.location.href = "/forms/envoyer";
}

function next_page(page) {
    window.location.href = "/forms/formulaire-page/" + page;
}

function previous_page(n) {
    window.location.href = "/forms/formulaire-page/" + (n - 1);
}

function printer() {
    console.log("aaaaaaa")
}