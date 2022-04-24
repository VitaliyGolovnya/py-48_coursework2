from community import Community


if __name__ == '__main__':
    with open('user_token.txt') as file:
        user_token = file.read()
    community = Community(user_token=user_token)
    community.longpolling()



