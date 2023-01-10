from geomstats_tools.parsing_utils import (
    add_updated_cls_to_source,
    find_class_lims,
    from_cls_dict_to_list,
    split_class,
)


def reorder_methods(cls_dict, order):
    # methods not in order are placed first
    cls_dict_ = {}
    to_order_dict = {}
    for key, value in cls_dict.items():
        if key in order:
            to_order_dict[key] = value
        else:
            cls_dict_[key] = value

    sorted_dict = {}
    for key in order:
        if key in to_order_dict:
            sorted_dict[key] = to_order_dict[key]

    cls_dict_.update(sorted_dict)
    return cls_dict_


def reorder_methods_given_source(source, class_name, methods_order):

    start_line, end_line = find_class_lims(class_name, source)
    cls_source = source[start_line:end_line]

    cls_dict = split_class(cls_source)
    cls_ordered_dict = reorder_methods(cls_dict, methods_order)
    ordered_cls_source = from_cls_dict_to_list(cls_ordered_dict)

    new_source = add_updated_cls_to_source(
        source, ordered_cls_source, start_line, end_line
    )

    return new_source
