
import os


def doc_validator(doc: str,extention :str):
    """
    Validates the input document name and returns the document name and its path.

    Args:
        doc (str): The input document name or path. The document can be provided
                    with or without the '.extention' extension.

    Returns:
        Tuple[str, str]: A tuple containing:
            - doc_name (str): The name of the document without the extension.
            - doc_path (str): The complete path to the document, ensuring the
                                '.extention' extension is added if it was missing.

    Raises:
        ValueError: If the file extension is invalid or if the specified path does not exist.
    """

    doc_path = doc

    path_to_doc, doc_name_full = os.path.split(doc)
    if path_to_doc == "":
        path_to_doc = "."
    elif not os.path.exists(path_to_doc):
        raise ValueError(f"oxd : given path {path_to_doc} does not exist")

    doc_name, ext = os.path.splitext(doc_name_full)

    if ext not in ["", extention]:
        raise ValueError(f"oxd : Invalid file extension. Only {extention} is allowed.")

    # Determine doc and doc_path based on the input
    if ext == extention:
        doc_path = doc
    else:
        doc_path = doc + extention

    return doc_name, doc_path