document.addEventListener('DOMContentLoaded', function() {
    const follow_button = document.querySelector('#follow_button')
    let editing=false
    document.querySelectorAll('.edit_content').forEach( textarea =>{
        textarea.style.display = 'none';
    })
    document.querySelectorAll('.edit_button').forEach( button =>{
        button.addEventListener('click', () =>{
            if (editing){
                return
            }
            editing = true
            const post = button.closest('.post')
            post.querySelector('.edit_content').style.display = 'block';
            post.querySelector('.edit_button').style.display = 'none';
            post.querySelector('.content').style.display = 'none';
            post.querySelector('textarea').value = post.querySelector('.content').textContent
        })
    })
    document.querySelectorAll('.edit_content').forEach( form =>{
        form.addEventListener('submit', event =>{
            event.preventDefault();
            const post_id=form.dataset.post
            const content = form.querySelector('textarea').value;
            if(content.length ===0){
                alert("Post cannot be empty");
                return;
            }
            else if(content.length >300){
                alert("Post cannot exceed 300 characters");
                return;
            }
            fetch(`/edit/${post_id}`, {
                method: 'PUT',
                body: JSON.stringify({
                    content
                })
            }).then( response =>{
                if(! response.ok){
                    throw new Error();
                }
                
            editing = false
            const post = form.closest('.post')
            post.querySelector('.edit_content').style.display = 'none';
            post.querySelector('.edit_button').style.display = 'inline-block';
            post.querySelector('.content').style.display = 'block';
            post.querySelector('.content').textContent = content;
            })
            .catch(() =>{
                alert("Error editing content")
            })
        })
    })

    document.querySelectorAll('.like_button').forEach( button =>{
        button.addEventListener('click', () =>{
            const count = button.closest('.post').querySelector('.likes');
            const state=button.dataset.status
            const post_id = button.dataset.post
            
            fetch(`/likes/${post_id}`, {
                method: 'PUT',
                body: JSON.stringify({
                    like_state: state
                })
            }).then( response =>{
                if(! response.ok){
                    throw new Error();
                }
                let countNum = parseInt(count.innerHTML);
                if (state == "true"){
                    button.innerHTML= "Like";
                    button.dataset.status = "false";
                    button.className="btn btn-sm btn-outline-primary like_button"
                    countNum--;
                    count.innerHTML=countNum;
                }
                else{
                    button.innerHTML ="Unlike";
                    button.dataset.status = "true";
                    button.className="btn btn-sm btn-outline-secondary like_button"
                    countNum++;
                    count.innerHTML=countNum;
                }

                
            }).catch(() =>{
                alert("Error Liking Post")
            })
            
        })
    })
    if(follow_button){
        follow_button.addEventListener('click', () =>{
            const state =follow_button.dataset.status;
            const userpage = follow_button.dataset.userpage;
            change_follow(userpage, state)
        })
    }

})


function change_follow(user_id, state){
    const follow_button = document.querySelector('#follow_button')
    fetch(`/follow/${user_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            following_state: state
        })
    }).then( response =>{
        if(! response.ok){
            throw new Error();
        }
        let countLink=document.querySelector('#followers_count').innerHTML;
        let countNum = parseInt(countLink);
        if (state == "true"){
            follow_button.innerHTML= "Follow";
            follow_button.dataset.status = "false";
            follow_button.className="btn btn-sm btn-outline-primary"
            countNum--;
            document.querySelector('#followers_count').innerHTML=countNum;
        }
        else{
            follow_button.innerHTML ="Unfollow";
            follow_button.dataset.status = "true";
            follow_button.className="btn btn-sm btn-outline-secondary"
            countNum++;
            document.querySelector('#followers_count').innerHTML=countNum;
        }

        
    }).catch(() =>{
        alert("Error Following User")
    })
}
