function clicked(tarefa_id, concluida){
    var csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    $.ajax({
        url: '/checklist/atualizar-tarefa/' + tarefa_id + '/',
        method: 'POST',
        data: {
            'remove': false,
            'concluida': !concluida,
            'csrfmiddlewaretoken': csrfToken  // Inclua o token CSRF aqui
        },
        success: function(data) {
            // Lida com a resposta do servidor (opcional)
            console.log(data.mensagem);
        },
        error: function(error) {
            console.error('Houve um erro:', error);
        }
    });
}
function deleteTarefa(tarefa_id){
    var csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    $.ajax({
        url: '/checklist/atualizar-tarefa/' + tarefa_id + '/',
        method: 'POST',
        data: {
            'remove': true,
            'csrfmiddlewaretoken': csrfToken  // Inclua o token CSRF aqui
        },
        success: function(data) {
            // Lida com a resposta do servidor (opcional)
            console.log(data.mensagem);
        },
        error: function(error) {
            console.error('Houve um erro:', error);
        }
    });
}