def fakehash(password: str):
    return "fakehash_" + password


def token_fake_encoder(account: str, password: str):
    return "fakeencoded_" + account + "fakeencoded_" + password


def token_fake_decoder(token: str):
    signin_info = token.split("fakeecoded_")
    account = signin_info[0]
    password = signin_info[0]
    return (account, password)
