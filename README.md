## Chat service
### This is a service that provides chat functionality. <br>

1. **Register a new channel**<br>
   Owner becomes a member of the channel. <br>
   URL: `/channels`<br>
   Method: `PUT`<br>
   Parameters: <br>

   | **Parameter** | **Type**  | **In**  | **Required** |
   |---------------|-----------|---------|--------------|
   | `id`          | string    | body    | no           |
   | `owner`       | string    | body    | yes          |
   | `topic `      | string    | body    | no           |
 
   Responses: <br>
   | Response         | Description                                  |
   |------------------|----------------------------------------------|
   | `201` `channelId`| Channel registered.                          |
   | `400`            | Invalid input, missing owner. Or the channel with such id already exists.|

2. **Get channel by ID**<br>
   URL: `/channels/{channelId}`<br>
   Method: `GET`<br>
   Parameters: <br>

   | **Parameter** | **Type**  | **In**  | **Required** |
   |---------------|-----------|---------|--------------|
   | `channelId`   | string    | path    | yes          |
 
   Responses: <br>
   | Response         | Description          |
   |------------------|----------------------|
   | `200`            | Channel details.     |
   | `404`            | Channel not found.   |

3. **Delete channel by ID**<br>
   Deletes a channel, all its messages and membership records. <br>
   URL: `/channels/{channelId}`<br>
   Method: `DELETE`<br>
   Parameters: <br>

   | **Parameter** | **Type**  | **In**  | **Required** |
   |---------------|-----------|---------|--------------|
   | `channelId`   | string    | path    | yes          |
 
   Responses: <br>
   | Response         | Description          |
   |------------------|----------------------|
   | `204`            | Channel deleted.     |
   | `404`            | Channel not found.   |

4. **Add message to channel**<br>
   URL: `/channels/{channelId}/messages`<br>
   Method: `PUT`<br>
   Parameters: <br>

   | **Parameter** | **Type**  | **In**  | **Required** |
   |---------------|-----------|---------|--------------|
   | `channelId`   | string    | path    | yes          |
   | `author`      | string    | body    | yes          |
   | `text`        | string    | body    | yes          |
 
   Responses: <br>
   | Response         | Description                              |
   |------------------|------------------------------------------|
   | `201`            | Message added.                           |
   | `400`            | Invalid input, missing text or author.   |

5. **Get messages from channel**<br>
   URL: `/channels/{channelId}/messages`<br>
   Method: `GET`<br>
   Parameters: <br>

   | **Parameter** | **Type**  | **In**  | **Required** |
   |---------------|-----------|---------|--------------|
   | `channelId`   | string    | path    | yes          |
   | `startAt`     | integer   | query   | no           |
   | `author`      | string    | query   | no           |
 
   Responses: <br>
   | Response         | Description                              |
   |------------------|------------------------------------------|
   | `200`            | List of messages.                        |

6. **Add member to channel**<br>
   URL: `/channels/{channelId}/members`<br>
   Method: `PUT`<br>
   Parameters: <br>

   | **Parameter** | **Type**  | **In**  | **Required** |
   |---------------|-----------|---------|--------------|
   | `channelId`   | string    | path    | yes          |
   | `member`      | string    | body    | yes          |
 
   Responses: <br>
   | Response         | Description                              |
   |------------------|------------------------------------------|
   | `201`            | Member added.                            |
   | `400`            | Invalid input, missing member. Or the member is already in the channel.  |

7. **Get members of channel**<br>
   URL: `/channels/{channelId}/members`<br>
   Method: `GET`<br>
   Parameters: <br>

   | **Parameter** | **Type**  | **In**  | **Required** |
   |---------------|-----------|---------|--------------|
   | `channelId`   | string    | path    | yes          |
 
   Responses: <br>
   | Response         | Description         |
   |------------------|---------------------|
   | `200`            | List of members.    |
   | `404`            | Channel not found.  |

8. **Remove member from channel**<br>
   URL: `/channels/{channelId}/members/{memberId}`<br>
   Method: `DELETE`<br>
   Parameters: <br>

   | **Parameter** | **Type**  | **In**  | **Required** |
   |---------------|-----------|---------|--------------|
   | `channelId`   | string    | path    | yes          |
   | `memberId`    | string    | path    | yes          |
 
   Responses: <br>
   | Response         | Description         |
   |------------------|---------------------|
   | `204`            | Member removed.     |
   | `404`            | Member not found.   |
