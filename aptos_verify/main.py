list_rules = [

]


def format_output_message(result: list):
    return result

async def process_rules():
    rs = []
    for rule in list_rules:
        try:
            rs.append(await rule())
        except BaseException as e:
            pass

    return format_output_message(rs)
