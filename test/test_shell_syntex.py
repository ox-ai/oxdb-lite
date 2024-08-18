from ox_db.shell.log import OxdbShell


def run(shell_command):
    oxdb_shell = OxdbShell('')
    shell_command = shell_command or 'oxdb get "mydb"'
    if oxdb_shell.validate_command(shell_command):
        translated = oxdb_shell.translate_command(shell_command)
        print(translated)

def test_oxdb_shell():
    oxdb_shell = OxdbShell(oxdb=None)  # Mock `oxdb` as None for testing purposes

    # Test cases for `oxdb.info()` command
    assert oxdb_shell.validate_command("oxdb.info")
    assert oxdb_shell.translate_command("oxdb.info") == "oxdb.info()"

    assert oxdb_shell.validate_command("info")
    assert oxdb_shell.translate_command("info") == "oxdb.info()"

    # Test cases for `oxdb.doc.info()` command
    assert oxdb_shell.validate_command("oxdb.doc.info")
    assert oxdb_shell.translate_command("oxdb.doc.info") == "oxdb.doc.info()"

    assert oxdb_shell.validate_command("doc.info")
    assert oxdb_shell.translate_command("doc.info") == "oxdb.doc.info()"

    assert oxdb_shell.validate_command("doc info")
    assert oxdb_shell.translate_command("doc info") == "oxdb.doc.info()"

    # Test cases for `oxdb.get_db("dbname")` command
    assert oxdb_shell.validate_command('oxdb.get("mydb")')
    assert oxdb_shell.translate_command('oxdb.get("mydb")') == 'oxdb.get_db("mydb")'

    assert oxdb_shell.validate_command('get("mydb")')
    assert oxdb_shell.translate_command('get("mydb")') == 'oxdb.get_db("mydb")'

    assert oxdb_shell.validate_command('oxdb get "mydb"')
    assert oxdb_shell.translate_command('oxdb get "mydb"') == 'oxdb.get_db("mydb")'

    assert oxdb_shell.validate_command('get "mydb"')
    assert oxdb_shell.translate_command('get "mydb"') == 'oxdb.get_db("mydb")'

    # Test cases for `oxdb.get_db("dbname","path")` command
    assert oxdb_shell.validate_command('oxdb.get("mydb","path")')
    assert (
        oxdb_shell.translate_command('oxdb.get("mydb","path")')
        == 'oxdb.get_db("mydb","path")'
    )

    assert oxdb_shell.validate_command('get("mydb","path")')
    assert (
        oxdb_shell.translate_command('get("mydb","path")')
        == 'oxdb.get_db("mydb","path")'
    )

    assert oxdb_shell.validate_command('oxdb get("mydb","path")')
    assert (
        oxdb_shell.translate_command('oxdb get("mydb","path")')
        == 'oxdb.get_db("mydb","path")'
    )

    assert oxdb_shell.validate_command('get("mydb","path")')
    assert (
        oxdb_shell.translate_command('get("mydb","path")')
        == 'oxdb.get_db("mydb","path")'
    )

    # Test cases for `oxdb.doc.get_doc("docname")` command
    assert oxdb_shell.validate_command('oxdb.doc.get("mydoc")')
    assert (
        oxdb_shell.translate_command('oxdb.doc.get("mydoc")')
        == 'oxdb.doc.get_doc("mydoc")'
    )

    assert oxdb_shell.validate_command('doc.get("mydoc")')
    assert (
        oxdb_shell.translate_command('doc.get("mydoc")') == 'oxdb.doc.get_doc("mydoc")'
    )

    assert oxdb_shell.validate_command('doc get "mydoc"')
    assert (
        oxdb_shell.translate_command('doc get "mydoc"') == 'oxdb.doc.get_doc("mydoc")'
    )

    # Test cases for `oxdb.doc.push(**data)` command
    data = '**{"uid": "177473", "document": "this is test document"}'
    assert oxdb_shell.validate_command(f"oxdb.doc.push({data})")
    assert (
        oxdb_shell.translate_command(f"oxdb.doc.push({data})")
        == f"oxdb.doc.push({data})"
    )

    assert oxdb_shell.validate_command(f"doc.push({data})")
    assert oxdb_shell.translate_command(f"doc.push({data})") == f"oxdb.doc.push({data})"

    assert oxdb_shell.validate_command(f"doc push({data})")
    assert oxdb_shell.translate_command(f"doc push({data})") == f"oxdb.doc.push({data})"

    assert oxdb_shell.validate_command(f"push({data})")
    assert oxdb_shell.translate_command(f"push({data})") == f"oxdb.doc.push({data})"

    # Test cases for `oxdb.doc.pull(**data)` command
    data = '**{"uid": "177473"}'
    assert oxdb_shell.validate_command(f"oxdb.doc.pull({data})")
    assert (
        oxdb_shell.translate_command(f"oxdb.doc.pull({data})")
        == f"oxdb.doc.pull({data})"
    )

    assert oxdb_shell.validate_command(f"doc.pull({data})")
    assert oxdb_shell.translate_command(f"doc.pull({data})") == f"oxdb.doc.pull({data})"

    assert oxdb_shell.validate_command(f"doc pull({data})")
    assert oxdb_shell.translate_command(f"doc pull({data})") == f"oxdb.doc.pull({data})"

    assert oxdb_shell.validate_command(f"pull({data})")
    assert oxdb_shell.translate_command(f"pull({data})") == f"oxdb.doc.pull({data})"

    # Test cases for `oxdb.doc.search(**data)` command
    data = '{"query": "test"}'
    assert oxdb_shell.validate_command(f"oxdb.doc.search({data})")
    assert (
        not oxdb_shell.translate_command(f"oxdb.doc.search({data})")
        == f"oxdb.doc.search(**{data})"
    )

    assert oxdb_shell.validate_command(f"doc.search({data})")
    assert (
        not oxdb_shell.translate_command(f"doc.search({data})")
        == f"oxdb.doc.search(**{data})"
    )

    assert oxdb_shell.validate_command(f"doc search({data})")
    assert (
        not oxdb_shell.translate_command(f"doc search({data})")
        == f"oxdb.doc.search(**{data})"
    )

    assert oxdb_shell.validate_command(f"search({data})")
    assert (
        not oxdb_shell.translate_command(f"search({data})")
        == f"oxdb.doc.search(**{data})"
    )

    print("All tests passed!")


# Run the test function
test_oxdb_shell()
