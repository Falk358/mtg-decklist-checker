def card_title_matches(card_title_decklist: str, card_title_banlist: str) -> bool:
    decklist_title_no_whitespace: list = card_title_decklist.split()
    banlist_title_no_whitespace: list = card_title_banlist.split()
    if len(decklist_title_no_whitespace) != len(banlist_title_no_whitespace):
        return False
    for index, item in enumerate(decklist_title_no_whitespace):
        if item.lower() != banlist_title_no_whitespace[index].lower():
            print(f"[INFO] {item} at index {index} doe not match {banlist_title_no_whitespace[index]}")
            return False

    return True
