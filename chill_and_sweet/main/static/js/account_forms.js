//Botones para editar los inputs
const name_btn = document.querySelector("#name_btn");
const lastname_btn = document.querySelector("#lastname_btn");
const email_btn = document.querySelector("#email_btn");

//Inputs para modificar información del usuario
const name = document.querySelector("#name");
const lastname = document.querySelector("#lastname");
const email = document.querySelector("#email");

//Boton para guardar los cambios en la información del usuario
const btn_save_changes = document.querySelector("#btn_save_changes");

//Formulario de información de cuenta del usuario
const info_user_form = document.querySelector(".info-user-form");

//Formulario de cambio de contraseña
const form_new_pass = document.querySelector(".form-new-pass");

//inputs auxiliares en el manejo de errores en la contraseña
const act_pass_error = document.querySelector("#act_pass_error");
const new_pass_error = document.querySelector("#new_pass_error");


name_btn.addEventListener("click", () => {
    if(name.disabled) {
        name.disabled = false;
        lastname.disabled = false;
        email.disabled = false;
        name.focus();
        btn_save_changes.style.display = "block";
    }
});

lastname_btn.addEventListener("click", () => {
    if(lastname.disabled) {
        name.disabled = false;
        lastname.disabled = false;
        email.disabled = false;
        lastname.focus();
        btn_save_changes.style.display = "block";
    }
});

email_btn.addEventListener("click", () => {
    if(email.disabled) {
        name.disabled = false;
        lastname.disabled = false;
        email.disabled = false;
        email.focus();
        btn_save_changes.style.display = "block";
    }
});


info_user_form.addEventListener("submit", (e) => {
    e.preventDefault();
    Swal.fire({
        position: "top",
        icon: "success",
        title: "Cambios realizados con éxito",
        showConfirmButton: false,
        timer: 2000
      }).then( () => {
        btn_save_changes.style.display = "none";
        info_user_form.submit();
      } );
});


