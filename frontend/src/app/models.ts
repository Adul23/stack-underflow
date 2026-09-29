export interface AuthToken{
    refresh:string;
    access:string;
}
export interface Comments {
    id: number;
    text: string;
    author: number;
    question: number;
    author_email : string;
    created_at : Date;
    update_at : Date;
}
export interface Questions {
    author_email?: string;
    author_name?: string;
    id: number;
    title: string;
    description: string;
    author: number;
    slug: string;
    tag: number[];
    created_at: Date;
    updated_at: Date;
    is_active: boolean;
}
export interface Tags {
    id: number;
    name: string;
    slug: string;
}
export interface Users {
    id: number,
    first_name: string,
    last_name: string,
    email: string,
    is_active : boolean,
    is_admin : boolean,
  }

export interface TagDetailResponse {
  tag: Tags;
  questions: Questions[];
}

export interface QuestionDetailResponse {
    question : Questions,
    comments : Comments[],
    tags : Tags[]
}
