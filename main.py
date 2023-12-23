import requests

token = "YOUR Github TOKEN"  # don't forget to give your token the access for unfollowing users in github settings
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}


def get_paginated_data(url):
    """
    Retrieve paginated data from a given GitHub API URL.

    Args:
        url (str): The GitHub API URL to retrieve data from.

    Returns:
        list: A list containing data retrieved from all paginated pages.
    """
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
    """
    Retrieve a list of followers for the authenticated GitHub user.

    Returns:
        list: A list of usernames representing followers.
    """
    url = "https://api.github.com/user/followers?per_page=100"
    data = get_paginated_data(url)
    return [user["login"] for user in data]


def get_followings():
    """
    Retrieve a list of users that the authenticated GitHub user is following.

    Returns:
        list: A list of usernames representing followings.
    """
    url = "https://api.github.com/user/following?per_page=100"
    data = get_paginated_data(url)
    return [user["login"] for user in data]


def get_ghost_users():
    """
    Identify users that the authenticated GitHub user is following but who are not following back.

    Returns:
        list: A list of usernames representing ghost users.
    """
    followers = get_followers()
    followings = get_followings()
    ghosts = list()

    for user in followings:
        if user not in followers:
            ghosts.append(user)

    return ghosts


while True:
    menu_text = """MENU OPTIONS:
    0. Exit
    1. List Followers
    2. List Followings
    3. Unfollow Users Not Following Back
    Enter the corresponding number:"""

    choice = input(menu_text)
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

            print(f"\n{ghosts_number} users have been removed.")
        else:
            print("\nCongrats! You have no ghost users.")

    elif choice == "0":
        print("Bye!")
        break

    else:
        print("Unknown Option Selected!\nPlease Try Again.")

    print("======================================================\n")
