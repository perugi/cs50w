document.addEventListener('DOMContentLoaded', function () {
    posts = document.querySelectorAll(".post");
    posts.forEach(post => {
        const edit_button = post.querySelector(".post-edit");
        if (edit_button !== null) {
            edit_button.addEventListener('click', () => edit_post_field(post))
        }

        const auth = document.querySelector("#is-authenticated");
        if (auth !== null) {
            const like_icon = post.querySelector(".like-icon");
            like_icon.addEventListener('click', () => like_post(post));
        }
    });
});

function edit_post_field(post) {
    const content = post.querySelector(".post-content");
    const existing_content = content.innerHTML;

    const edit_form = document.createElement("div");
    edit_form.className = "edit-form";

    const edit_input = document.createElement("textarea");
    edit_input.className = "form-control edit-field";
    edit_input.rows = 3;
    edit_input.value = existing_content;
    edit_form.appendChild(edit_input);

    const edit_button = document.createElement("button");
    edit_button.innerHTML = "Edit";
    edit_button.id = "edit-button";
    edit_button.className = "btn btn-primary my-2";
    edit_button.addEventListener('click', () => edit_post(post));
    edit_form.appendChild(edit_button);

    post.replaceChild(edit_form, content);
};

function edit_post(post) {
    const edit_form = post.querySelector(".edit-form");
    const timestamp = post.querySelector(".post-timestamp");

    // Make the changes on the front-end.
    const new_content = post.querySelector(".edit-field").value;
    const content = document.createElement("div");
    content.className = "post-content";
    content.innerHTML = post.querySelector(".edit-field").value;

    const time = new Date();
    timestamp.innerHTML = `${format_time(time)} (edited)`

    post.replaceChild(content, edit_form);

    // Make a PUT call to edit the post in the database.
    fetch('/edit_post', {
        method: 'PUT',
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
    let new_status = false;

    // Make the changes on the front-end.
    // User does not like the post yet, add to the like count and bold it, create the user-liked hidden element.
    if (user_liked === null) {
        like_count.innerHTML = Number(like_count.innerHTML) + 1;

        like_count.classList.remove("not-liked");
        like_count.classList.add("liked");

        const user_liked_new = document.createElement("div");
        user_liked_new.className = "user-liked";
        user_liked_new.setAttribute("type", "hidden");
        post_likes.append(user_liked_new);

        new_status = true;
    }

    else {
        like_count.innerHTML = Number(like_count.innerHTML) - 1;
        like_count.classList.remove("liked");
        like_count.classList.add("not-liked");
        user_liked.remove();

        new_status = false;
    }

    // Make a PUT call to like/unlike the post in the database. We use the same link for liking/unliking,
    // as it toggles the status of the like for the logged in user. The new_status is sent for verification only.
    fetch('/like_post', {
        method: 'PUT',
        body: JSON.stringify({
            id: post.id,
            new_status: new_status
        })
    })
        .then(response => response.json())
        .then(result => {
            console.log(result)
        })
}

function format_time(time) {
    var months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    options = {
        month: "short",
        hour: "numeric",
        minute: "numeric"
    }

    let formatted_time = `${months[time.getMonth()]}. ${time.getDate()}, ${time.getFullYear()}, `;
    if (time.getHours() === 0) {
        formatted_time += `12:${time.getMinutes().toString().padStart(2, '0')} a.m.`
    }
    else if (time.getHours() < 12) {
        formatted_time += `${time.getHours()}:${time.getMinutes().toString().padStart(2, '0')} a.m.`
    }
    else if (time.getHours() === 12) {
        formatted_time += `${time.getHours()}:${time.getMinutes().toString().padStart(2, '0')} p.m.`
    }
    else {
        formatted_time += `${time.getHours() - 12}:${time.getMinutes().toString().padStart(2, '0')} p.m.`
    }

    return formatted_time;
}