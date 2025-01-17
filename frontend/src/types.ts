export interface IHobby {
  id: number;
  name: string;
}

export interface IUser {
  id: number;
  username: string;
  name: string;
  email: string;
  date_of_birth?: string;
  hobbies: string[];
}

export interface IFriendRequestPayload {
  friend_request_id: number;
  action: string;
}

export interface IUserUpdate extends IUser {
  password?: string;
}
