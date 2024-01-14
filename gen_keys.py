from pathlib import Path

data_path = Path("data")
data_path.mkdir(exist_ok=True)
private_key_path = data_path / "private_key"
public_key_path = data_path / "public_key"


def gen_keys():
    from Crypto.PublicKey import RSA

    key = RSA.generate(2048)
    private_key = key.export_key().decode("utf-8")
    public_key = key.publickey().export_key().decode("utf-8")

    if private_key_path.is_file() and public_key_path.is_file():
        print("Keys already exist")
        return
    with open(private_key_path, "w") as f:
        f.write(private_key)
    with open(public_key_path, "w") as f:
        f.write(public_key)


if __name__ == "__main__":
    gen_keys()
