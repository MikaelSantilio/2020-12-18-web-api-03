from django.core.exceptions import ValidationError
from core.models import Profile, Post, Comment


def bind_id_with_objects(id_dict, objects_list):
    i = 0
    for _id in id_dict:
        id_dict[_id] = objects_list[i]
        i += 1

    return id_dict


def remove_unvalid_objects(objects_list):
    for i in range(len(objects_list)):
        try:
            objects_list[i].full_clean()
        except ValidationError:
            objects_list[i] = None

    return objects_list


def save_users(data_users):
    cleaned_users = []
    id_users = {}

    for obj in data_users:
        obj["street"] = obj["address"]["street"]
        obj["city"] = obj["address"]["city"]
        obj["zipcode"] = obj["address"]["zipcode"]

        id_users[obj["id"]] = obj["id"]

        cleaned_users.append(
            Profile(
                name=obj["name"],
                email=obj["email"],
                street=obj["street"],
                city=obj["city"],
                zipcode=obj["zipcode"]))

    response_users = Profile.objects.bulk_create(cleaned_users, ignore_conflicts=True)
    response_users = remove_unvalid_objects(response_users)

    response_users = Profile.objects.order_by('-pk')[:len(response_users)]
    response_users = list(reversed(response_users))

    id_users = bind_id_with_objects(id_users, response_users)

    return id_users, response_users


def save_posts(data_posts, id_users):

    cleaned_posts = []
    id_posts = {}

    for obj in data_posts:
        if not id_users[obj["userId"]]:
            continue

        obj["user"] = id_users[obj["userId"]]

        id_posts[obj["id"]] = obj["id"]

        cleaned_posts.append(
            Post(
                title=obj["title"],
                body=obj["body"],
                user=obj["user"]))

    response_posts = Post.objects.bulk_create(cleaned_posts, ignore_conflicts=True)
    response_posts = remove_unvalid_objects(response_posts)

    response_posts = Post.objects.order_by('-pk')[:len(response_posts)]
    response_posts = list(reversed(response_posts))

    id_posts = bind_id_with_objects(id_posts, response_posts)

    return id_posts, response_posts


def save_comments(data_comments, id_posts):
    cleaned_comments = []

    for obj in data_comments:
        if not id_posts[obj["postId"]]:
            continue

        obj["post"] = id_posts[obj["postId"]]

        cleaned_comments.append(
            Comment(
                name=obj["name"],
                email=obj["email"],
                body=obj["body"],
                post=obj["post"]))

    response_comments = Comment.objects.bulk_create(cleaned_comments, ignore_conflicts=True)
    response_comments = remove_unvalid_objects(response_comments)

    return response_comments


def save_json_db(data):

    id_users, response_users = save_users(data["users"])
    id_posts, response_posts = save_posts(data["posts"], id_users)
    response_comments = save_comments(data["comments"], id_posts)

    return {
        "users": response_users,
        "comments": response_comments,
        "posts": response_posts
    }
