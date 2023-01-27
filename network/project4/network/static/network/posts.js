document.addEventListener('DOMContentLoaded', function () {
    posts = document.querySelectorAll(".post");
    posts.forEach(post => {
        const edit_button = post.querySelector(".post-edit");
        if (edit_button !== null) {
            edit_button.addEventListener('click', () => edit_post_field(post))
        }

        const like_icon = post.querySelector(".like-icon");
        like_icon.addEventListener('click', () => like_post(post))
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

function like_post(post) {
    const post_likes = post.querySelector(".post-likes");
    const like_count = post.querySelector(".like-count");
    const user_liked = post.querySelector(".user-liked");

    // Make the changes on the front-end.
    // User does not like the post yet, add to the like count and bold it, create the user-liked hidden element.
    if (user_liked === null) {
        like_count.innerHTML = Number(like_count.innerHTML) + 1;

        like_count.classList.add("liked");

        const user_liked_new = document.createElement("div");
        user_liked_new.className = "user-liked";
        user_liked_new.setAttribute("type", "hidden");
        post_likes.append(user_liked_new);
    }

    else {
        like_count.innerHTML = Number(like_count.innerHTML) - 1;
        like_count.classList.remove("liked");
        user_liked.remove();
    }

    // Make a call to edit the likes in the database.
    // TODO
}   