export interface IHobby {
    id: number;
    name: string;
  }
  
  export interface IUser {
    id: number;
    username: string;
    name: string;
    email: string;
    date_of_birth?: string; // or null
    hobbies: string[];      // store hobby names
    common_hobbies?: number; // only used in user list responses
  }
  
  export interface IFriendRequestPayload {
    friend_request_id: number;
    action: string;
  }
  