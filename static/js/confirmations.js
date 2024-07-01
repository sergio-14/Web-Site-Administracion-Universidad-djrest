function confirmReactivar(userId) {
    swal({
        title: "¿Estás seguro?",
        text: "¿Deseas reactivar este usuario?",
        icon: "warning",
        buttons: true,
        dangerMode: true,
    })
    .then((willReactivate) => {
        if (willReactivate) {
            window.location.href = "/usuarios/" + userId + "/reactivar/";
        }
    });
}

function confirmDelete(userId) {
    swal({
        title: "¿Estás seguro?",
        text: "Este usuario quedará inactivo.",
        icon: "warning",
        buttons: true,
        dangerMode: true,
    })
    .then((willDelete) => {
        if (willDelete) {
            window.location.href = "/usuarios/" + userId + "/eliminar/";
        }
    });
}

function confirmCreate() {
    swal({
        title: "¿Está seguro?",
        text: "¿Desea crear este usuario?",
        icon: "warning",
        buttons: true,
        dangerMode: true,
    })
    .then((willCreate) => {
        if (willCreate) {
            document.getElementById('create-user-form').submit();
        }
    });
}

//confiaciones global campos 


