export type OrganizationMembershipRole =
  | "owner"
  | "admin"
  | "implementation_manager"
  | "support"
  | "viewer";

export interface AuthMembership {
  organization_id: string;
  organization_name: string;
  role: OrganizationMembershipRole;
}

export interface AuthUser {
  id: string;
  email: string;
  full_name: string;
  status: string;
  is_platform_admin: boolean;
  last_login_at: string | null;
  memberships: AuthMembership[];
}

export interface AuthSession {
  id: string;
  user_id: string;
  expires_at: string;
  revoked_at: string | null;
  last_used_at: string | null;
  created_at: string;
  updated_at: string;
}

export interface AuthTokenResponse {
  access_token: string;
  token_type: "bearer";
  expires_at: string;
  user: AuthUser;
  session: AuthSession;
}

export interface AuthMeResponse {
  user: AuthUser;
}

export interface AuthLoginPayload {
  email: string;
  password: string;
}

export interface AuthRegisterPayload extends AuthLoginPayload {
  full_name: string;
  organization_name: string;
  membership_role?: OrganizationMembershipRole;
  is_platform_admin?: boolean;
}
