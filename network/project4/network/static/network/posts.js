document.addEventListener('DOMContentLoaded', function () {
    console.log("posts loaded");
    posts = document.querySelectorAll(".post");
    // posts_arr = [...posts]
    posts.forEach(post => {
        const edit_button = post.querySelector(".post-edit");
        if (edit_button !== null) {
            edit_button.addEventListener('click', () => edit_post_field(post))
        }
    });
});

function edit_post_field(post) {
    const content = post.querySelector(".post-content");
    const existing_content = content.innerHTML;

    const edit_form = document.createElement("div");
    edit_form.className = "edit-form";

    const edit_input = document.createElement("textarea");
    edit_input.className = "edit-field";
    edit_input.value = existing_content;
    edit_form.appendChild(edit_input);

    const edit_button = document.createElement("button");
    edit_button.innerHTML = "Edit";
    edit_button.className = "btn btn-primary";
    edit_button.addEventListener('click', () => edit_post(post));
    edit_form.appendChild(edit_button);

    post.replaceChild(edit_form, content);
};

function edit_post(post) {
    const edit_form = post.querySelector(".edit-form");

    // Make the changes on the front-end.
    const new_content = post.querySelector(".edit-field").value;
    const content = document.createElement("div");
    content.className = "post-content";
    content.innerHTML = post.querySelector(".edit-field").value;

    post.replaceChild(content, edit_form);

    // Make a POST call to edit the post in the database.
    fetch('/edit_post', {
        method: 'POST',
        body: JSON.stringify({
            id: post.id,
            new_content: new_content
        })
    })
        .then(response => response.json())
        .then(result => {
            console.log(result)
        })
}