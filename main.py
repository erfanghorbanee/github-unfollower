import requests

token = "YOUR Github TOKEN"  # don't forget to give your token the access for unfollwing users in github settings
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}


def getPaginatedData(url):
    pagesRemaining = True
    data = list()

    while pagesRemaining:
        r = requests.get(url, headers=headers)
        data += r.json()

        if r.links.get("next"):
            url = r.links["next"]["url"]
        else:
            pagesRemaining = False

    return data


def get_followers():
    url = "https://api.github.com/user/followers?per_page=100"
    data = getPaginatedData(url)
    followers = list()

    for user in data:
        followers.append(user["login"])

    return followers


def get_followings():
    url = "https://api.github.com/user/following?per_page=100"
    data = getPaginatedData(url)
    followings = list()

    for user in data:
        followings.append(user["login"])

    return followings


def get_ghost_users():
    followers = get_followers()
    followings = get_followings()
    ghosts = list()

    for user in followings:
        if user not in followers:
            ghosts.append(user)

    return ghosts


while True:
    menue_text = """ENTER A NUMBER FROM THE OPTIONS BELOW:
0. Exit
1. List your followers
2. List your followings
3. Unfollow the users that didn't follow you back
"""
    choice = input(menue_text)
    if choice == "1":
        followers = get_followers()
        for user in followers:
            print(user)
        print("\nTotal number of followers:", len(followers))

    elif choice == "2":
        followings = get_followings()
        for user in followings:
            print(user)
        print("\nTotal number of followings:", len(followings))

    elif choice == "3":
        ghosts = get_ghost_users()
        ghosts_number = len(ghosts)
        if ghosts_number:
            for user in ghosts:
                url = f"https://api.github.com/user/following/{user}"
                r = requests.delete(url, headers=headers)
                print(user)

            print(f"\n{ghosts_number} users has been removed.")
        else:
            print("\nCongrats! You have no ghost users.")

    elif choice == "0":
        print("Bye!")
        break

    else:
        print("Unknown Option Selected!\nPlease Try Again.")

    print("======================================================\n")
