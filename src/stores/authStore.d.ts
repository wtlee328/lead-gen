import type { User, Session, AuthError } from '@supabase/supabase-js';
export declare const useAuthStore: import("pinia").StoreDefinition<"auth", Pick<{
    user: import("vue").Ref<{
        id: string;
        app_metadata: {
            [x: string]: any;
            provider?: string | undefined;
        };
        user_metadata: import("@supabase/auth-js").UserMetadata;
        aud: string;
        confirmation_sent_at?: string | undefined;
        recovery_sent_at?: string | undefined;
        email_change_sent_at?: string | undefined;
        new_email?: string | undefined;
        new_phone?: string | undefined;
        invited_at?: string | undefined;
        action_link?: string | undefined;
        email?: string | undefined;
        phone?: string | undefined;
        created_at: string;
        confirmed_at?: string | undefined;
        email_confirmed_at?: string | undefined;
        phone_confirmed_at?: string | undefined;
        last_sign_in_at?: string | undefined;
        role?: string | undefined;
        updated_at?: string | undefined;
        identities?: {
            id: string;
            user_id: string;
            identity_data?: {
                [key: string]: any;
            } | undefined;
            identity_id: string;
            provider: string;
            created_at?: string | undefined;
            last_sign_in_at?: string | undefined;
            updated_at?: string | undefined;
        }[] | undefined;
        is_anonymous?: boolean | undefined;
        is_sso_user?: boolean | undefined;
        factors?: {
            id: string;
            friendly_name?: string | undefined;
            factor_type: "totp" | "phone" | (string & {});
            status: "verified" | "unverified";
            created_at: string;
            updated_at: string;
        }[] | undefined;
    } | null, User | {
        id: string;
        app_metadata: {
            [x: string]: any;
            provider?: string | undefined;
        };
        user_metadata: import("@supabase/auth-js").UserMetadata;
        aud: string;
        confirmation_sent_at?: string | undefined;
        recovery_sent_at?: string | undefined;
        email_change_sent_at?: string | undefined;
        new_email?: string | undefined;
        new_phone?: string | undefined;
        invited_at?: string | undefined;
        action_link?: string | undefined;
        email?: string | undefined;
        phone?: string | undefined;
        created_at: string;
        confirmed_at?: string | undefined;
        email_confirmed_at?: string | undefined;
        phone_confirmed_at?: string | undefined;
        last_sign_in_at?: string | undefined;
        role?: string | undefined;
        updated_at?: string | undefined;
        identities?: {
            id: string;
            user_id: string;
            identity_data?: {
                [key: string]: any;
            } | undefined;
            identity_id: string;
            provider: string;
            created_at?: string | undefined;
            last_sign_in_at?: string | undefined;
            updated_at?: string | undefined;
        }[] | undefined;
        is_anonymous?: boolean | undefined;
        is_sso_user?: boolean | undefined;
        factors?: {
            id: string;
            friendly_name?: string | undefined;
            factor_type: "totp" | "phone" | (string & {});
            status: "verified" | "unverified";
            created_at: string;
            updated_at: string;
        }[] | undefined;
    } | null>;
    session: import("vue").Ref<{
        provider_token?: string | null | undefined;
        provider_refresh_token?: string | null | undefined;
        access_token: string;
        refresh_token: string;
        expires_in: number;
        expires_at?: number | undefined;
        token_type: string;
        user: {
            id: string;
            app_metadata: {
                [x: string]: any;
                provider?: string | undefined;
            };
            user_metadata: import("@supabase/auth-js").UserMetadata;
            aud: string;
            confirmation_sent_at?: string | undefined;
            recovery_sent_at?: string | undefined;
            email_change_sent_at?: string | undefined;
            new_email?: string | undefined;
            new_phone?: string | undefined;
            invited_at?: string | undefined;
            action_link?: string | undefined;
            email?: string | undefined;
            phone?: string | undefined;
            created_at: string;
            confirmed_at?: string | undefined;
            email_confirmed_at?: string | undefined;
            phone_confirmed_at?: string | undefined;
            last_sign_in_at?: string | undefined;
            role?: string | undefined;
            updated_at?: string | undefined;
            identities?: {
                id: string;
                user_id: string;
                identity_data?: {
                    [key: string]: any;
                } | undefined;
                identity_id: string;
                provider: string;
                created_at?: string | undefined;
                last_sign_in_at?: string | undefined;
                updated_at?: string | undefined;
            }[] | undefined;
            is_anonymous?: boolean | undefined;
            is_sso_user?: boolean | undefined;
            factors?: {
                id: string;
                friendly_name?: string | undefined;
                factor_type: "totp" | "phone" | (string & {});
                status: "verified" | "unverified";
                created_at: string;
                updated_at: string;
            }[] | undefined;
        };
    } | null, Session | {
        provider_token?: string | null | undefined;
        provider_refresh_token?: string | null | undefined;
        access_token: string;
        refresh_token: string;
        expires_in: number;
        expires_at?: number | undefined;
        token_type: string;
        user: {
            id: string;
            app_metadata: {
                [x: string]: any;
                provider?: string | undefined;
            };
            user_metadata: import("@supabase/auth-js").UserMetadata;
            aud: string;
            confirmation_sent_at?: string | undefined;
            recovery_sent_at?: string | undefined;
            email_change_sent_at?: string | undefined;
            new_email?: string | undefined;
            new_phone?: string | undefined;
            invited_at?: string | undefined;
            action_link?: string | undefined;
            email?: string | undefined;
            phone?: string | undefined;
            created_at: string;
            confirmed_at?: string | undefined;
            email_confirmed_at?: string | undefined;
            phone_confirmed_at?: string | undefined;
            last_sign_in_at?: string | undefined;
            role?: string | undefined;
            updated_at?: string | undefined;
            identities?: {
                id: string;
                user_id: string;
                identity_data?: {
                    [key: string]: any;
                } | undefined;
                identity_id: string;
                provider: string;
                created_at?: string | undefined;
                last_sign_in_at?: string | undefined;
                updated_at?: string | undefined;
            }[] | undefined;
            is_anonymous?: boolean | undefined;
            is_sso_user?: boolean | undefined;
            factors?: {
                id: string;
                friendly_name?: string | undefined;
                factor_type: "totp" | "phone" | (string & {});
                status: "verified" | "unverified";
                created_at: string;
                updated_at: string;
            }[] | undefined;
        };
    } | null>;
    loading: import("vue").Ref<boolean, boolean>;
    error: import("vue").Ref<AuthError | {
        name: string;
        message: string;
    } | null, AuthError | {
        name: string;
        message: string;
    } | null>;
    isAuthenticated: import("vue").ComputedRef<boolean>;
    initializeAuth: () => Promise<void>;
    signUp: (emailInput: string, passwordInput: string) => Promise<{
        user: User | null;
        session: Session | null;
    } | null>;
    signIn: (emailInput: string, passwordInput: string) => Promise<{
        user: User;
        session: Session;
        weakPassword?: import("@supabase/auth-js").WeakPassword;
    } | null>;
    signOut: () => Promise<void>;
}, "user" | "session" | "loading" | "error">, Pick<{
    user: import("vue").Ref<{
        id: string;
        app_metadata: {
            [x: string]: any;
            provider?: string | undefined;
        };
        user_metadata: import("@supabase/auth-js").UserMetadata;
        aud: string;
        confirmation_sent_at?: string | undefined;
        recovery_sent_at?: string | undefined;
        email_change_sent_at?: string | undefined;
        new_email?: string | undefined;
        new_phone?: string | undefined;
        invited_at?: string | undefined;
        action_link?: string | undefined;
        email?: string | undefined;
        phone?: string | undefined;
        created_at: string;
        confirmed_at?: string | undefined;
        email_confirmed_at?: string | undefined;
        phone_confirmed_at?: string | undefined;
        last_sign_in_at?: string | undefined;
        role?: string | undefined;
        updated_at?: string | undefined;
        identities?: {
            id: string;
            user_id: string;
            identity_data?: {
                [key: string]: any;
            } | undefined;
            identity_id: string;
            provider: string;
            created_at?: string | undefined;
            last_sign_in_at?: string | undefined;
            updated_at?: string | undefined;
        }[] | undefined;
        is_anonymous?: boolean | undefined;
        is_sso_user?: boolean | undefined;
        factors?: {
            id: string;
            friendly_name?: string | undefined;
            factor_type: "totp" | "phone" | (string & {});
            status: "verified" | "unverified";
            created_at: string;
            updated_at: string;
        }[] | undefined;
    } | null, User | {
        id: string;
        app_metadata: {
            [x: string]: any;
            provider?: string | undefined;
        };
        user_metadata: import("@supabase/auth-js").UserMetadata;
        aud: string;
        confirmation_sent_at?: string | undefined;
        recovery_sent_at?: string | undefined;
        email_change_sent_at?: string | undefined;
        new_email?: string | undefined;
        new_phone?: string | undefined;
        invited_at?: string | undefined;
        action_link?: string | undefined;
        email?: string | undefined;
        phone?: string | undefined;
        created_at: string;
        confirmed_at?: string | undefined;
        email_confirmed_at?: string | undefined;
        phone_confirmed_at?: string | undefined;
        last_sign_in_at?: string | undefined;
        role?: string | undefined;
        updated_at?: string | undefined;
        identities?: {
            id: string;
            user_id: string;
            identity_data?: {
                [key: string]: any;
            } | undefined;
            identity_id: string;
            provider: string;
            created_at?: string | undefined;
            last_sign_in_at?: string | undefined;
            updated_at?: string | undefined;
        }[] | undefined;
        is_anonymous?: boolean | undefined;
        is_sso_user?: boolean | undefined;
        factors?: {
            id: string;
            friendly_name?: string | undefined;
            factor_type: "totp" | "phone" | (string & {});
            status: "verified" | "unverified";
            created_at: string;
            updated_at: string;
        }[] | undefined;
    } | null>;
    session: import("vue").Ref<{
        provider_token?: string | null | undefined;
        provider_refresh_token?: string | null | undefined;
        access_token: string;
        refresh_token: string;
        expires_in: number;
        expires_at?: number | undefined;
        token_type: string;
        user: {
            id: string;
            app_metadata: {
                [x: string]: any;
                provider?: string | undefined;
            };
            user_metadata: import("@supabase/auth-js").UserMetadata;
            aud: string;
            confirmation_sent_at?: string | undefined;
            recovery_sent_at?: string | undefined;
            email_change_sent_at?: string | undefined;
            new_email?: string | undefined;
            new_phone?: string | undefined;
            invited_at?: string | undefined;
            action_link?: string | undefined;
            email?: string | undefined;
            phone?: string | undefined;
            created_at: string;
            confirmed_at?: string | undefined;
            email_confirmed_at?: string | undefined;
            phone_confirmed_at?: string | undefined;
            last_sign_in_at?: string | undefined;
            role?: string | undefined;
            updated_at?: string | undefined;
            identities?: {
                id: string;
                user_id: string;
                identity_data?: {
                    [key: string]: any;
                } | undefined;
                identity_id: string;
                provider: string;
                created_at?: string | undefined;
                last_sign_in_at?: string | undefined;
                updated_at?: string | undefined;
            }[] | undefined;
            is_anonymous?: boolean | undefined;
            is_sso_user?: boolean | undefined;
            factors?: {
                id: string;
                friendly_name?: string | undefined;
                factor_type: "totp" | "phone" | (string & {});
                status: "verified" | "unverified";
                created_at: string;
                updated_at: string;
            }[] | undefined;
        };
    } | null, Session | {
        provider_token?: string | null | undefined;
        provider_refresh_token?: string | null | undefined;
        access_token: string;
        refresh_token: string;
        expires_in: number;
        expires_at?: number | undefined;
        token_type: string;
        user: {
            id: string;
            app_metadata: {
                [x: string]: any;
                provider?: string | undefined;
            };
            user_metadata: import("@supabase/auth-js").UserMetadata;
            aud: string;
            confirmation_sent_at?: string | undefined;
            recovery_sent_at?: string | undefined;
            email_change_sent_at?: string | undefined;
            new_email?: string | undefined;
            new_phone?: string | undefined;
            invited_at?: string | undefined;
            action_link?: string | undefined;
            email?: string | undefined;
            phone?: string | undefined;
            created_at: string;
            confirmed_at?: string | undefined;
            email_confirmed_at?: string | undefined;
            phone_confirmed_at?: string | undefined;
            last_sign_in_at?: string | undefined;
            role?: string | undefined;
            updated_at?: string | undefined;
            identities?: {
                id: string;
                user_id: string;
                identity_data?: {
                    [key: string]: any;
                } | undefined;
                identity_id: string;
                provider: string;
                created_at?: string | undefined;
                last_sign_in_at?: string | undefined;
                updated_at?: string | undefined;
            }[] | undefined;
            is_anonymous?: boolean | undefined;
            is_sso_user?: boolean | undefined;
            factors?: {
                id: string;
                friendly_name?: string | undefined;
                factor_type: "totp" | "phone" | (string & {});
                status: "verified" | "unverified";
                created_at: string;
                updated_at: string;
            }[] | undefined;
        };
    } | null>;
    loading: import("vue").Ref<boolean, boolean>;
    error: import("vue").Ref<AuthError | {
        name: string;
        message: string;
    } | null, AuthError | {
        name: string;
        message: string;
    } | null>;
    isAuthenticated: import("vue").ComputedRef<boolean>;
    initializeAuth: () => Promise<void>;
    signUp: (emailInput: string, passwordInput: string) => Promise<{
        user: User | null;
        session: Session | null;
    } | null>;
    signIn: (emailInput: string, passwordInput: string) => Promise<{
        user: User;
        session: Session;
        weakPassword?: import("@supabase/auth-js").WeakPassword;
    } | null>;
    signOut: () => Promise<void>;
}, "isAuthenticated">, Pick<{
    user: import("vue").Ref<{
        id: string;
        app_metadata: {
            [x: string]: any;
            provider?: string | undefined;
        };
        user_metadata: import("@supabase/auth-js").UserMetadata;
        aud: string;
        confirmation_sent_at?: string | undefined;
        recovery_sent_at?: string | undefined;
        email_change_sent_at?: string | undefined;
        new_email?: string | undefined;
        new_phone?: string | undefined;
        invited_at?: string | undefined;
        action_link?: string | undefined;
        email?: string | undefined;
        phone?: string | undefined;
        created_at: string;
        confirmed_at?: string | undefined;
        email_confirmed_at?: string | undefined;
        phone_confirmed_at?: string | undefined;
        last_sign_in_at?: string | undefined;
        role?: string | undefined;
        updated_at?: string | undefined;
        identities?: {
            id: string;
            user_id: string;
            identity_data?: {
                [key: string]: any;
            } | undefined;
            identity_id: string;
            provider: string;
            created_at?: string | undefined;
            last_sign_in_at?: string | undefined;
            updated_at?: string | undefined;
        }[] | undefined;
        is_anonymous?: boolean | undefined;
        is_sso_user?: boolean | undefined;
        factors?: {
            id: string;
            friendly_name?: string | undefined;
            factor_type: "totp" | "phone" | (string & {});
            status: "verified" | "unverified";
            created_at: string;
            updated_at: string;
        }[] | undefined;
    } | null, User | {
        id: string;
        app_metadata: {
            [x: string]: any;
            provider?: string | undefined;
        };
        user_metadata: import("@supabase/auth-js").UserMetadata;
        aud: string;
        confirmation_sent_at?: string | undefined;
        recovery_sent_at?: string | undefined;
        email_change_sent_at?: string | undefined;
        new_email?: string | undefined;
        new_phone?: string | undefined;
        invited_at?: string | undefined;
        action_link?: string | undefined;
        email?: string | undefined;
        phone?: string | undefined;
        created_at: string;
        confirmed_at?: string | undefined;
        email_confirmed_at?: string | undefined;
        phone_confirmed_at?: string | undefined;
        last_sign_in_at?: string | undefined;
        role?: string | undefined;
        updated_at?: string | undefined;
        identities?: {
            id: string;
            user_id: string;
            identity_data?: {
                [key: string]: any;
            } | undefined;
            identity_id: string;
            provider: string;
            created_at?: string | undefined;
            last_sign_in_at?: string | undefined;
            updated_at?: string | undefined;
        }[] | undefined;
        is_anonymous?: boolean | undefined;
        is_sso_user?: boolean | undefined;
        factors?: {
            id: string;
            friendly_name?: string | undefined;
            factor_type: "totp" | "phone" | (string & {});
            status: "verified" | "unverified";
            created_at: string;
            updated_at: string;
        }[] | undefined;
    } | null>;
    session: import("vue").Ref<{
        provider_token?: string | null | undefined;
        provider_refresh_token?: string | null | undefined;
        access_token: string;
        refresh_token: string;
        expires_in: number;
        expires_at?: number | undefined;
        token_type: string;
        user: {
            id: string;
            app_metadata: {
                [x: string]: any;
                provider?: string | undefined;
            };
            user_metadata: import("@supabase/auth-js").UserMetadata;
            aud: string;
            confirmation_sent_at?: string | undefined;
            recovery_sent_at?: string | undefined;
            email_change_sent_at?: string | undefined;
            new_email?: string | undefined;
            new_phone?: string | undefined;
            invited_at?: string | undefined;
            action_link?: string | undefined;
            email?: string | undefined;
            phone?: string | undefined;
            created_at: string;
            confirmed_at?: string | undefined;
            email_confirmed_at?: string | undefined;
            phone_confirmed_at?: string | undefined;
            last_sign_in_at?: string | undefined;
            role?: string | undefined;
            updated_at?: string | undefined;
            identities?: {
                id: string;
                user_id: string;
                identity_data?: {
                    [key: string]: any;
                } | undefined;
                identity_id: string;
                provider: string;
                created_at?: string | undefined;
                last_sign_in_at?: string | undefined;
                updated_at?: string | undefined;
            }[] | undefined;
            is_anonymous?: boolean | undefined;
            is_sso_user?: boolean | undefined;
            factors?: {
                id: string;
                friendly_name?: string | undefined;
                factor_type: "totp" | "phone" | (string & {});
                status: "verified" | "unverified";
                created_at: string;
                updated_at: string;
            }[] | undefined;
        };
    } | null, Session | {
        provider_token?: string | null | undefined;
        provider_refresh_token?: string | null | undefined;
        access_token: string;
        refresh_token: string;
        expires_in: number;
        expires_at?: number | undefined;
        token_type: string;
        user: {
            id: string;
            app_metadata: {
                [x: string]: any;
                provider?: string | undefined;
            };
            user_metadata: import("@supabase/auth-js").UserMetadata;
            aud: string;
            confirmation_sent_at?: string | undefined;
            recovery_sent_at?: string | undefined;
            email_change_sent_at?: string | undefined;
            new_email?: string | undefined;
            new_phone?: string | undefined;
            invited_at?: string | undefined;
            action_link?: string | undefined;
            email?: string | undefined;
            phone?: string | undefined;
            created_at: string;
            confirmed_at?: string | undefined;
            email_confirmed_at?: string | undefined;
            phone_confirmed_at?: string | undefined;
            last_sign_in_at?: string | undefined;
            role?: string | undefined;
            updated_at?: string | undefined;
            identities?: {
                id: string;
                user_id: string;
                identity_data?: {
                    [key: string]: any;
                } | undefined;
                identity_id: string;
                provider: string;
                created_at?: string | undefined;
                last_sign_in_at?: string | undefined;
                updated_at?: string | undefined;
            }[] | undefined;
            is_anonymous?: boolean | undefined;
            is_sso_user?: boolean | undefined;
            factors?: {
                id: string;
                friendly_name?: string | undefined;
                factor_type: "totp" | "phone" | (string & {});
                status: "verified" | "unverified";
                created_at: string;
                updated_at: string;
            }[] | undefined;
        };
    } | null>;
    loading: import("vue").Ref<boolean, boolean>;
    error: import("vue").Ref<AuthError | {
        name: string;
        message: string;
    } | null, AuthError | {
        name: string;
        message: string;
    } | null>;
    isAuthenticated: import("vue").ComputedRef<boolean>;
    initializeAuth: () => Promise<void>;
    signUp: (emailInput: string, passwordInput: string) => Promise<{
        user: User | null;
        session: Session | null;
    } | null>;
    signIn: (emailInput: string, passwordInput: string) => Promise<{
        user: User;
        session: Session;
        weakPassword?: import("@supabase/auth-js").WeakPassword;
    } | null>;
    signOut: () => Promise<void>;
}, "initializeAuth" | "signUp" | "signIn" | "signOut">>;
