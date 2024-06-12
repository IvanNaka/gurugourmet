// Constante para pegar os Elementos
const getElement = (pegandoElemento) => {
    const element = document.querySelector(pegandoElemento);
    if (element) return element;
    throw Error(`Erro ao tentar encontrar a classe. Não existe uma classe chamada "${pegandoElemento}".`);
}

// Constante para pegar os Links
const links = getElement('.nav-links');
const navBtnDOM = getElement('.nav-btn');

// Event Listener para os botões - toda vez que clica ele da um toggle..
navBtnDOM.addEventListener('click', () => {
    links.classList.toggle('show-links');
});

// Constante para a data no footer
const data = getElement('#data');
const anoAtual = new Date().getFullYear();
data.textContent = anoAtual;

// ------------------------------------------------------------------------------------------
// Ingredientes
// ------------------------------------------------------------------------------------------

function criarItemIngrediente(ingrediente) {
    // Cria um novo elemento de div para o item de ingrediente
    const novoItem = document.createElement('div');
    novoItem.classList.add('ingredient-item');
    // Cria um novo elemento de span para o nome do ingrediente
    const novoTexto = document.createElement('span');
    novoTexto.textContent = ingrediente.nome;
    novoTexto.id = ingrediente.id;
    novoTexto.classList.add('ingredient-text'); // Adiciona uma classe ao elemento de texto

    // Cria um novo elemento de ícone do Font Awesome para representar o botão de remoção
    const iconeRemover = document.createElement('i');
    iconeRemover.classList.add('fa', 'fa-rectangle-xmark');
    // Adiciona um ouvinte de evento para o ícone de remoção
    iconeRemover.addEventListener('click', function() {
        removerIngrediente(novoItem);
    });

    // Adiciona o texto e o ícone de remoção ao novo item de ingrediente
    novoItem.appendChild(novoTexto);
    novoItem.appendChild(iconeRemover);

    return novoItem;
}

// Função para adicionar um ingrediente à lista
function adicionarIngrediente() {
    // Tem que tirar isso aqui depois e colocar vindo do banco de dados
    var ingredientesDisponiveis = getListaIngredientes()
    // Captura o valor do input de ingrediente
    const inputIngrediente = document.querySelector('.ingredientInput');
    const novoIngrediente = inputIngrediente.value.trim();
    // Verifica se o ingrediente está presente na lista de ingredientes4
    var ingredienteObj = verificarIngrediente(novoIngrediente, ingredientesDisponiveis)
    if (ingredienteObj) {
        // Cria um novo item de ingrediente
        const novoItem = criarItemIngrediente(ingredienteObj);
        // Adiciona o novo item de ingrediente à lista de ingredientes
        const listaIngredientes = document.getElementById('listaIngredientes');
        listaIngredientes.appendChild(novoItem);

        // Limpa o valor do input
        inputIngrediente.value = '';
    } else {
        // Ingrediente não encontrado, exibe uma mensagem de erro
        alert('Ingrediente não encontrado. Por favor, digite um ingrediente válido.');
        // Você também pode exibir a mensagem de erro em um elemento na página, em vez de usar alert
    }
}

// Função para remover um ingrediente da lista
function removerIngrediente(item) {
    item.remove();
}

function login() {
    var formData = new FormData();
    formData.append('email', document.getElementById('email').value);
    formData.append('password', document.getElementById('password').value);
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/login/', true);
    xhr.setRequestHeader('X-CSRFToken', '{{ csrf_token }}'); // Adicione o token CSRF, necessário para Django
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                location.href = '../';
            } else {
                document.getElementById('error-message').innerText = JSON.parse(xhr.response).error;
            }
        }
    };
    xhr.send(formData);
}
function getListaIngredientes() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/ingredientes/', false); // Alterado para true para fazer uma requisição assíncrona
    xhr.send(); // Enviar a requisição
    if (xhr.status === 200) {
        var response = JSON.parse(xhr.responseText).lista_ingredientes; // Corrigido o acesso ao responseText
        return response; // Chama o callback com null para o erro e o response para os dados
    } else {
        console.log('Erro ao trazer ingredientes');
        return []
    }
}
function validateEmail(email) {
    var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
}

function validatePassword(password) {
    var regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
    return regex.test(password);
}
function cadastro() {
    var email = document.getElementById('email').value;
    if (!validateEmail(email)) {
        document.getElementById('error-message').textContent = 'Endereço de e-mail inválido';
        return;
    }
    if (!validatePassword(document.getElementById('password').value)) {
        document.getElementById('error-message').textContent = 'A senha deve conter pelo menos 8 caracteres, uma letra maiúscula, uma letra minúscula, um número e um caractere especial';
        return;
    }
    var formData = new FormData();
    formData.append('email', document.getElementById('email').value);
    formData.append('instagram', document.getElementById('instagram').value);
    formData.append('password', document.getElementById('password').value);
    formData.append('username', document.getElementById('username').value);
    formData.append('data_aniversario', document.getElementById('data_aniversario').value);

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/cadastro/', true);
    xhr.setRequestHeader('X-CSRFToken', '{{ csrf_token }}'); // Adicione o token CSRF, necessário para Django
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                location.href = '../';
            } else {
                document.getElementById('error-message').innerText = JSON.parse(xhr.response).error;
            }
        }
    };
    xhr.send(formData);
}
function reset() {
    var email = document.getElementById('email').value;
    if (!validateEmail(email)) {
        document.getElementById('error-message').textContent = 'Endereço de e-mail inválido';
        return;
    }
    if (!validatePassword(document.getElementById('password').value)) {
        document.getElementById('error-message').textContent = 'A senha deve conter pelo menos 8 caracteres, uma letra maiúscula, uma letra minúscula, um número e um caractere especial';
        return;
    }
    var formData = new FormData();
    formData.append('email', document.getElementById('email').value);
    formData.append('instagram', document.getElementById('instagram').value);
    formData.append('password', document.getElementById('password').value);
    formData.append('username', document.getElementById('username').value);

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/reset/', true);
    xhr.setRequestHeader('X-CSRFToken', '{{ csrf_token }}'); // Adicione o token CSRF, necessário para Django
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                location.href = '../';
            } else {
                document.getElementById('error-message').innerText = JSON.parse(xhr.response).error;
            }
        }
    };
    xhr.send(formData);
}


// Função para verificar se o ingrediente está no banco de dados
function verificarIngrediente(ingrediente, ingredientesDisponiveis) {
    // Verifica se o ingrediente está na lista de ingredientes disponíveis
    var ingredienteVerificado = null;
    ingredientesDisponiveis.forEach(
        (element) => {
            if (element.nome === ingrediente) {
                ingredienteVerificado = element
            }
        }
    )
    return ingredienteVerificado
}

// Adiciona um ouvinte de evento para o botão "Adicionar"
document.getElementById('searchButton').addEventListener('click', adicionarIngrediente);

// Adiciona um ouvinte de evento para o input de ingrediente
const inputIngrediente = document.querySelector('.ingredientInput');
inputIngrediente.addEventListener('keyup', function(event) {
    // Verifica se a tecla pressionada foi a tecla "Enter" (código 13)
    if (event.keyCode === 13) {
        // Chama a função para adicionar o ingrediente
        adicionarIngrediente();
    }
});


document.getElementById('botaoPesquisar').addEventListener('click', function() {
        // Get the list of ingredients
        var lista_ingredientes = [];
        var listaIngredientesElements = document.querySelectorAll('#listaIngredientes *');

        listaIngredientesElements.forEach(function(element) {
            var id = element.id; // Adjust this line if the id is stored in a different way
            lista_ingredientes.push(id);
        });

        lista_ingredientes = lista_ingredientes.map(Number);
        // Send the AJAX request
        fetch('/receita/lista', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'lista_ingredientes': lista_ingredientes
            })
        })
        .then(response => response.json())
        .then(data => {
        // Handle the response data here
        console.log(data);

        // Get the lista-container element
        var listaContainer = document.querySelector('.lista-container');

        // Clear the current content
        listaContainer.innerHTML = '';

        // Add new content from the fetched data
        // This assumes that the data is an array of objects with 'titulo', 'tempo_preparo', and 'imagem_principal' properties
        data.lista_receitas.forEach(function(receita) {
            var receitaElement = document.createElement('a');
            receitaElement.href = "/receita/" + receita.id;
            receitaElement.className = "receita";

            var imgElement = document.createElement('img');
            imgElement.src = receita.imagem_principal;
            imgElement.className = "img receita-img";
            receitaElement.appendChild(imgElement);

            var titleElement = document.createElement('h5');
            titleElement.textContent = receita.titulo;
            receitaElement.appendChild(titleElement);

            var timeElement = document.createElement('p');
            timeElement.textContent = "Tempo de Preparo: " + receita.tempo_preparo;
            receitaElement.appendChild(timeElement);

            listaContainer.appendChild(receitaElement);
        });
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});

// ------------------------------------------------------------------------------------------
// Formulario
// ------------------------------------------------------------------------------------------

function submitForm(event) {
    event.preventDefault(); // Previne o envio padrão do formulário

    // Chama a função de validação
    if (validaInputVazio()) {
        const form = document.getElementById("myForm");
        const formData = new FormData(form);

        // Enviar os dados do formulário para o Django via AJAX
        fetch("receitas/", {
            method: "POST",
            body: formData
        })
        .then(response => {
            if (response.ok) {
                // Redirecionar ou exibir mensagem de sucesso após o envio bem-sucedido
                console.log("Dados enviados com sucesso!");
            } else {
                // Exibir mensagem de erro se houver algum problema
                console.error("Erro ao enviar dados:", response.statusText);
            }
        })
        .catch(error => {
            console.error("Erro ao enviar dados:", error);
        });
    }
}

// ------------------------------------------------------------------------------------------
// Login
// ------------------------------------------------------------------------------------------

function validaInputVazio() {
    var email = document.getElementById("email").value;
    var password = document.getElementById("password").value;

    if (email === "" || password === "") {
        alert("Por favor, preencha todos os campos");
        return false;
    } else {
        return true;
    }
}

function submitForm(event) {
    event.preventDefault(); 

    if (validaInputVazio()) {
        // Aqui você pode adicionar a lógica para enviar os dados do formulário para o backend
        console.log("Formulário válido. Enviando dados...");
    }
}


