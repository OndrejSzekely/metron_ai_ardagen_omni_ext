"""
Implements utilities for the extension.
"""
import typing


def get_data_type(data_list: typing.List[typing.Any]) -> typing.Any:  # pylint: disable=too-many-branches
    """
    Obtain data types.

    Args:
        data_list (List[Any]): List of objects.

    Raises:
        ValueError: Raised if list items are of different data types or non supported types are present.

    Returns:
        Any: Base data type of the items in the list.
    """
    first_el = data_list[0]
    if isinstance(first_el, (list, tuple)):
        el_len = len(first_el)
        el_type = type(first_el[0])
    else:
        el_len = ""  # type: ignore
        el_type = type(first_el)

    for list_item in data_list:
        if isinstance(list_item, (list, tuple)):
            curr_type = type(list_item[0])
        else:
            curr_type = type(list_item)

        if curr_type != el_type:
            # Don't raise error if one of the type is float/int and the other is int/float.
            if (curr_type == int or curr_type == float) and (  # pylint: disable=consider-using-in
                el_type == int or el_type == float  # pylint: disable=consider-using-in
            ):
                el_type = float
            else:
                raise ValueError("Every element in the items provided must be the same type.")

    if el_type == int:
        base_type = f"int{el_len}"
    elif el_type == float:
        base_type = f"double{el_len}"
    elif el_type == bool:
        base_type = "bool"
    elif el_type == str:
        base_type = "token"
    else:
        raise ValueError(
            f"Base type {el_type} is not supported. Only elements of type str, bool, int and float are supported."
        )
    return base_type
