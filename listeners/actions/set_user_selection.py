from logging import Logger
from slack_bolt import Ack
from state_store.set_redis_user_state import set_redis_user_state


def set_user_selection(logger: Logger, ack: Ack, body: dict):
    try:
        ack()
        user_id = body["user"]["id"]
        value = body["actions"][0]["selected_option"]["value"]
        if value != "null":
            # parsing the selected option value from the options array in app_home_opened.py
            selected_provider, selected_model = value.split(" ")[-1], value.split(" ")[0]
            set_redis_user_state(user_id, selected_provider, selected_model)
            logger.info(f"Set Redis state for user {user_id}: provider={selected_provider}, model={selected_model}")
        else:
            raise ValueError("Please make a selection")
    except Exception as e:
        logger.error(f"Error in set_user_selection: {e}")
