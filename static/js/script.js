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

function criarItemIngrediente(nomeIngrediente) {
    // Cria um novo elemento de div para o item de ingrediente
    const novoItem = document.createElement('div');
    novoItem.classList.add('ingredient-item');

    // Cria um novo elemento de span para o nome do ingrediente
    const novoTexto = document.createElement('span');
    novoTexto.textContent = nomeIngrediente;
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
    const ingredientesDisponiveis = ["Cenoura", "Tomate", "Cebola", "Alho", "Pimentão", "Batata", "Abobrinha", "Brócolis", "Couve", "Salsinha", "Cebolinha", "Manjericão", "Coentro", "Alface", "Rúcula", "Espinafre", "Milho", "Ervilha", "Feijão", "Grão-de-bico"];

    // Captura o valor do input de ingrediente
    const inputIngrediente = document.querySelector('.ingredientInput');
    const novoIngrediente = inputIngrediente.value.trim();

    // Verifica se o ingrediente está presente no banco de dados
    if (verificarIngrediente(novoIngrediente, ingredientesDisponiveis)) {
        // Cria um novo item de ingrediente
        const novoItem = criarItemIngrediente(novoIngrediente);

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
function cadastro() {
    var formData = new FormData();
    formData.append('email', document.getElementById('email').value);
    formData.append('password', document.getElementById('password').value);
    formData.append('username', document.getElementById('username').value);
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


// Função para verificar se o ingrediente está no banco de dados
function verificarIngrediente(ingrediente, ingredientesDisponiveis) {
    // Verifica se o ingrediente está na lista de ingredientes disponíveis
    if (ingredientesDisponiveis.includes(ingrediente)) {
        return true; // Ingrediente encontrado
    } else {
        return false; // Ingrediente não encontrado
    }
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
        fetch("url_do_seu_endpoint_no_django/", {
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