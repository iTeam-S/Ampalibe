Messenger API 
=============

list of methods for sending messages to messenger

send_message
____________

This method allows you to send a text message to the given recipient,
Note that the number of characters to send is limited to 2000 characters


**Ref**: https://developers.facebook.com/docs/messenger-platform/send-messages#sending_text

**Args**:

    dest_id (str): user id facebook for the destination

    message (str): message want to send

**Example**:

.. code-block:: python

    chat.send_message('1444555414', "Hello world")