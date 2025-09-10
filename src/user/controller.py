from fastapi import Query, HTTPException, Depends
from starlette.responses import JSONResponse
from src.user.models import (
    User,
    UserProfile,
)
from src.config.postgres import get_db
from sqlalchemy.orm import Session
from src.user.utils import get_password_hash, verify_password
from src.auth.handler import get_current_user
from src.user.schemas import (
    ok,
    formatError,
    actionTransformUserLogin,
    actionTransformUser,
    mapUserProfileData,
    UserCreate,
    UserUpdate,
    UserLogin,
    PasswordUpdate,
    PasswordUpdateByUsername,
)
from src.constants import (
    HTTP_BAD_REQUEST,
    HTTP_BAD_REQUEST,
    HTTP_OK,
    HTTP_CREATED,
    HTTP_ACCEPTED,
    CURRENT_DATETIME,
    HTTP_NOT_FOUND,
    HTTP_UNAUTHORIZED,
)
from datetime import date, datetime
from src.utils.validate import validateEmail
from sqlalchemy import or_
import uuid


class UserController:
    @staticmethod
    async def register(
        request: UserCreate,
        authorization: str,
        db: Session = Depends(get_db),
    ) -> JSONResponse:
        try:
            userData: any = None
            userId: str = None
            if authorization:
                token = authorization.split("Bearer")[1].strip()
                userId = get_current_user(token)
                if userId:
                    userData = db.query(User).filter(User.id == userId).first()

            username = request.username.strip()
            password = request.password.strip()
            nama_lengkap = request.nama_lengkap.strip()
            email = request.email.strip()
            isEmailValid = validateEmail(email)

            if isEmailValid == False:
                raise HTTPException(
                    status_code=HTTP_BAD_REQUEST,
                    detail="Email tidak valid!",
                )
            if username == "":
                raise HTTPException(
                    status_code=HTTP_BAD_REQUEST,
                    detail="Username couldn't be empty!",
                )
            elif len(password) < 8:
                raise HTTPException(
                    status_code=HTTP_BAD_REQUEST,
                    detail="password must be at least 8 characters!",
                )

            existing_email = (
                db.query(UserProfile)
                .filter(UserProfile.email == email, UserProfile.deleted == False)
                .first()
            )

            if existing_email:
                raise HTTPException(
                    status_code=HTTP_BAD_REQUEST,
                    detail=f"Email : {email} already exists!",
                )

            userData = (
                db.query(User).filter(User.id == userId, User.deleted == False).first()
            )

            existing_user = db.query(User).filter(User.username == username).first()
            if existing_user and existing_user.deleted == False:
                raise HTTPException(
                    status_code=HTTP_BAD_REQUEST,
                    detail="Username already exists!",
                )

            hashPassword = get_password_hash(password)

            id_user = uuid.uuid4().hex
            if userData:
                existing_username = userData.username
                userMap = User(
                    id=id_user,
                    username=username,
                    password=hashPassword,
                    is_active=True,
                    created_by=existing_username,
                    created_date=CURRENT_DATETIME,
                )

                idProfile = uuid.uuid4().hex
                profileMap = UserProfile(
                    id=idProfile,
                    id_user=id_user,
                    nama_lengkap=nama_lengkap,
                    email=email,
                    created_by=existing_username,
                    created_date=CURRENT_DATETIME,
                )

                db.add(userMap)
                db.add(profileMap)
                db.commit()

                transformer = actionTransformUser(userMap, profileMap)
                return ok(transformer, "Successfully Create User!", HTTP_CREATED)
            else:
                raise HTTPException(
                    status_code=HTTP_BAD_REQUEST,
                    detail="You can register as super admin without login or login and than add new user except user admin!",
                )
        except HTTPException as e:
            db.rollback()
            return formatError("", e.detail, e.status_code)
        except Exception as e:
            db.rollback()
            return formatError("", str(e), HTTP_BAD_REQUEST)

    @staticmethod
    async def update(
        id: str,
        request: UserUpdate,
        authorization: str,
        db: Session = Depends(get_db),
    ) -> JSONResponse:
        try:
            if not authorization:
                raise HTTPException(
                    status_code=HTTP_UNAUTHORIZED,
                    detail="Authorization token is missing!",
                )

            token = authorization.split("Bearer")[1].strip()
            userId = get_current_user(token)
            if userId is None:
                raise HTTPException(
                    status_code=HTTP_UNAUTHORIZED,
                    detail="You are not logged in!",
                )

            isEmailValid = validateEmail(request.email)
            if isEmailValid == False:
                raise HTTPException(
                    status_code=HTTP_BAD_REQUEST,
                    detail="Email tidak valid!",
                )

            existing_email = (
                db.query(UserProfile, User)
                .join(User, User.id == UserProfile.id_user)
                .filter(
                    UserProfile.email == request.email,
                    User.id != id,
                    UserProfile.deleted.is_(False),
                )
                .first()
            )

            if existing_email is not None:
                raise HTTPException(
                    status_code=HTTP_BAD_REQUEST,
                    detail=f"Email : {request.email} already exists!",
                )

            existing_user = (
                db.query(User).filter(User.id == id, User.deleted == False).first()
            )

            if existing_user is None:
                raise HTTPException(
                    status_code=HTTP_NOT_FOUND,
                    detail=f"User with id {id} not found!",
                )

            existing_user_profile = (
                db.query(UserProfile)
                .filter(UserProfile.id_user == id, UserProfile.deleted == False)
                .first()
            )

            if existing_user_profile is None:
                raise HTTPException(
                    status_code=HTTP_NOT_FOUND,
                    detail="Your profile not found!",
                )

            user_data = (
                db.query(User).filter(User.id == userId, User.deleted == False).first()
            )

            if not user_data:
                raise HTTPException(
                    status_code=HTTP_UNAUTHORIZED,
                    detail="Session has ended, please login again!",
                )

            current_user = user_data

            userQuery = (
                db.query(User, UserProfile)
                .join(UserProfile, UserProfile.id_user == id)
                .filter(
                    User.deleted == False,
                    UserProfile.deleted == False,
                    User.id == id,
                )
                .first()
            )

            if not userQuery:
                raise HTTPException(
                    status_code=HTTP_NOT_FOUND, detail="User data not found!"
                )

            update_user, _, _, update_user_profile = userQuery

            # Validate and update fields if provided
            def validate_and_update(data, field, value, validation=None):
                if value != "":
                    if value is not None:
                        if validation and not validation(value):
                            raise HTTPException(
                                status_code=HTTP_BAD_REQUEST,
                                detail=f"{field} validation failed!",
                            )
                        data[field] = value

            update_data = {}
            profile_update_data = {}

            validate_and_update(update_data, "username", request.username.strip())

            validate_and_update(
                profile_update_data, "nama_lengkap", request.nama_lengkap
            )
            validate_and_update(profile_update_data, "email", request.email)

            # Set common update fields
            def set_common_fields(data):
                data["updated_date"] = CURRENT_DATETIME
                data["updated_by"] = current_user.username

            if update_data:
                set_common_fields(update_data)
                db.query(User).filter(User.id == id).update(update_data)

            if profile_update_data:
                set_common_fields(profile_update_data)
                db.query(UserProfile).filter(
                    UserProfile.id == update_user_profile.id
                ).update(profile_update_data)

            db.commit()

            return ok(
                "",
                f"User with name {request.nama_lengkap} update successfully!",
                HTTP_OK,
            )
        except HTTPException as e:
            db.rollback()
            return formatError("", e.detail, e.status_code)
        except Exception as e:
            db.rollback()
            return formatError("", str(e), HTTP_BAD_REQUEST)

    @staticmethod
    async def delete(
        id: str,
        authorization: str,
        db: Session = Depends(get_db),
    ) -> JSONResponse:
        try:
            token = authorization.split("Bearer")[1].strip()
            userId = get_current_user(token)

            if userId is None:
                raise HTTPException(
                    status_code=HTTP_UNAUTHORIZED,
                    detail="You are not logged in!",
                )

            user = (
                db.query(User).filter(User.id == userId, User.deleted == False).first()
            )

            if not user:
                raise HTTPException(
                    status_code=HTTP_UNAUTHORIZED,
                    detail="Session has ended, please login again!",
                )

            existing_user = (
                db.query(User).filter(User.id == id, User.deleted == False).first()
            )

            if existing_user is None:
                raise HTTPException(
                    status_code=HTTP_NOT_FOUND,
                    detail=f"User with id {id} not found!",
                )

            userQuery = (
                db.query(User, UserProfile)
                .join(UserProfile, UserProfile.id_user == id)
                .filter(
                    User.deleted == False,
                    UserProfile.deleted == False,
                    User.id == id,
                )
                .first()
            )

            if not userQuery:
                raise HTTPException(
                    status_code=HTTP_NOT_FOUND, detail="User query data not found!"
                )

            _, user_profile = userQuery

            # Perform updates in a single transaction
            db.query(UserProfile).filter(UserProfile.id == user_profile.id).update(
                {
                    "deleted": True,
                    "updated_date": CURRENT_DATETIME,
                    "updated_by": user.username,
                }
            )
            db.query(User).filter(User.id == id).update(
                {
                    "deleted": True,
                    "updated_date": CURRENT_DATETIME,
                    "updated_by": user.username,
                    "is_active": False,
                }
            )

            db.commit()
            return ok("", "Profile soft deleted successfully!", HTTP_OK)
        except HTTPException as e:
            db.rollback()
            return formatError("", e.detail, e.status_code)
        except Exception as e:
            db.rollback()
            return formatError("", str(e), HTTP_BAD_REQUEST)

    @staticmethod
    async def login(
        request: UserLogin,
        db: Session = Depends(get_db),
    ) -> JSONResponse:
        try:
            username = request.username.strip()
            password = request.password.strip()

            if username == "":
                raise HTTPException(
                    status_code=HTTP_BAD_REQUEST,
                    detail="username couldn't be empty!",
                )
            elif len(password) < 8:
                raise HTTPException(
                    status_code=HTTP_BAD_REQUEST,
                    detail="password must be at least 8 characters!",
                )

            userQuery = (
                db.query(User, UserProfile)
                .join(UserProfile, UserProfile.id_user == User.id)
                .filter(User.username == username, User.deleted == False)
                .first()
            )

            if userQuery is None:
                raise HTTPException(
                    status_code=HTTP_NOT_FOUND,
                    detail="user not found!",
                )

            user = userQuery

            if user is None:
                raise HTTPException(
                    status_code=HTTP_NOT_FOUND,
                    detail="user not found!",
                )

            if user.is_active == False:
                raise HTTPException(
                    status_code=HTTP_BAD_REQUEST,
                    detail="Your account is no longer active!",
                )

            transformerUserLoginUser = actionTransformUserLogin(user)

            verifyPasword = verify_password(
                password, transformerUserLoginUser["password"]
            )

            if verifyPasword == False:
                raise HTTPException(
                    status_code=HTTP_BAD_REQUEST,
                    detail="password yang di input salah!",
                )

            return ok(transformerUserLoginUser, "Successfully Login!", HTTP_ACCEPTED)
        except HTTPException as e:
            db.rollback()
            return formatError("", e.detail, e.status_code)
        except Exception as e:
            db.rollback()
            return formatError("", str(e), HTTP_BAD_REQUEST)

    @staticmethod
    async def profile(
        authorization: str,
        db: Session = Depends(get_db),
    ) -> JSONResponse:
        try:
            token = authorization.split("Bearer")[1].strip()
            userId = get_current_user(token)

            if userId is None:
                raise HTTPException(
                    status_code=HTTP_UNAUTHORIZED,
                    detail="You are not logged in!",
                )

            user = (
                db.query(User, UserProfile)
                .join(UserProfile, UserProfile.id_user == User.id)
                .filter(
                    UserProfile.deleted == False,
                    User.deleted == False,
                    User.id == userId,
                )
                .first()
            )

            if not user:
                raise HTTPException(
                    status_code=HTTP_NOT_FOUND,
                    detail="User profile not found!",
                )

            transformer = mapUserProfileData(user)
            return ok(transformer, "Successfully Get user Profile!", HTTP_OK)
        except HTTPException as e:
            db.rollback()
            return formatError("", e.detail, e.status_code)
        except Exception as e:
            db.rollback()
            return formatError("", str(e), HTTP_BAD_REQUEST)

    @staticmethod
    async def updatePassword(
        request: PasswordUpdate,
        authorization: str,
        db: Session = Depends(get_db),
    ) -> JSONResponse:
        try:
            if not authorization:
                raise HTTPException(
                    status_code=HTTP_UNAUTHORIZED,
                    detail="Authorization token is missing!",
                )

            token = authorization.split("Bearer")[1].strip()
            userId = get_current_user(token)
            if userId is None:
                raise HTTPException(
                    status_code=HTTP_UNAUTHORIZED,
                    detail="You are not logged in!",
                )

            if not request:
                raise HTTPException(
                    status_code=HTTP_BAD_REQUEST,
                    detail="Request body cannot be empty!",
                )

            # Fetch the current user data from the database
            user_data = (
                db.query(User).filter(User.id == userId, User.deleted == False).first()
            )

            if not user_data:
                raise HTTPException(
                    status_code=HTTP_NOT_FOUND,
                    detail="User not found!",
                )

            if request.new_password != request.confirm_new_password:
                raise HTTPException(
                    status_code=HTTP_BAD_REQUEST,
                    detail="New password and Confirm new password do not match!",
                )

            if not verify_password(request.old_password, user_data.password):
                raise HTTPException(
                    status_code=HTTP_BAD_REQUEST,
                    detail="Old password is incorrect!",
                )

            update_data = {}

            new_password = request.new_password
            if new_password:
                if len(new_password) < 8:
                    raise HTTPException(
                        status_code=HTTP_BAD_REQUEST,
                        detail="Password must be at least 8 characters long!",
                    )
                update_data["password"] = get_password_hash(new_password)

            def set_common_fields(data):
                data["updated_date"] = CURRENT_DATETIME
                data["updated_by"] = user_data.username

            if update_data:
                set_common_fields(update_data)
                db.query(User).filter(User.id == userId).update(update_data)

            db.commit()

            return ok("", "Update password successfully!", HTTP_OK)
        except HTTPException as e:
            db.rollback()
            return formatError("", e.detail, e.status_code)
        except Exception as e:
            db.rollback()
            return formatError("", str(e), HTTP_BAD_REQUEST)

    @staticmethod
    async def updatePasswordById(
        id: str,
        request: PasswordUpdate,
        authorization: str,
        db: Session = Depends(get_db),
    ) -> JSONResponse:
        try:
            if not authorization:
                raise HTTPException(
                    status_code=HTTP_UNAUTHORIZED,
                    detail="Authorization token is missing!",
                )

            token = authorization.split("Bearer")[1].strip()
            userId = get_current_user(token)
            if userId is None:
                raise HTTPException(
                    status_code=HTTP_UNAUTHORIZED,
                    detail="You are not logged in!",
                )

            if not request:
                raise HTTPException(
                    status_code=HTTP_BAD_REQUEST,
                    detail="Request body cannot be empty!",
                )

            # Fetch the current user data from the database
            user_data = (
                db.query(User).filter(User.id == id, User.deleted == False).first()
            )

            if not user_data:
                raise HTTPException(
                    status_code=HTTP_NOT_FOUND,
                    detail="User not found!",
                )

            if request.new_password != request.confirm_new_password:
                raise HTTPException(
                    status_code=HTTP_BAD_REQUEST,
                    detail="New password and Confirm new password do not match!",
                )

            if not verify_password(request.old_password, user_data.password):
                raise HTTPException(
                    status_code=HTTP_BAD_REQUEST,
                    detail="Old password is incorrect!",
                )

            update_data = {}

            new_password = request.new_password
            if new_password:
                if len(new_password) < 8:
                    raise HTTPException(
                        status_code=HTTP_BAD_REQUEST,
                        detail="Password must be at least 8 characters long!",
                    )
                update_data["password"] = get_password_hash(new_password)

            def set_common_fields(data):
                data["updated_date"] = CURRENT_DATETIME
                data["updated_by"] = user_data.username

            if update_data:
                set_common_fields(update_data)
                db.query(User).filter(User.id == userId).update(update_data)

            db.commit()

            return ok("", "Update password successfully!", HTTP_OK)
        except HTTPException as e:
            db.rollback()
            return formatError("", e.detail, e.status_code)
        except Exception as e:
            db.rollback()
            return formatError("", str(e), HTTP_BAD_REQUEST)

    @staticmethod
    async def updatePasswordByUsername(
        request: PasswordUpdateByUsername,
        authorization: str,
        db: Session = Depends(get_db),
    ) -> JSONResponse:
        try:
            if not authorization:
                raise HTTPException(
                    status_code=HTTP_UNAUTHORIZED,
                    detail="Authorization token is missing!",
                )

            token = authorization.split("Bearer")[1].strip()
            userId = get_current_user(token)
            if userId is None:
                raise HTTPException(
                    status_code=HTTP_UNAUTHORIZED,
                    detail="You are not logged in!",
                )

            if not request:
                raise HTTPException(
                    status_code=HTTP_BAD_REQUEST,
                    detail="Request body cannot be empty!",
                )

            # Fetch the current user data from the database
            user_data = (
                db.query(User)
                .filter(
                    User.username == request.username.strip(), User.deleted == False
                )
                .first()
            )

            if not user_data:
                raise HTTPException(
                    status_code=HTTP_NOT_FOUND,
                    detail="User not found!",
                )

            if request.new_password != request.confirm_new_password:
                raise HTTPException(
                    status_code=HTTP_BAD_REQUEST,
                    detail="New password and Confirm new password do not match!",
                )

            if not verify_password(request.old_password, user_data.password):
                raise HTTPException(
                    status_code=HTTP_BAD_REQUEST,
                    detail="Old password is incorrect!",
                )

            update_data = {}

            new_password = request.new_password
            if new_password:
                if len(new_password) < 8:
                    raise HTTPException(
                        status_code=HTTP_BAD_REQUEST,
                        detail="Password must be at least 8 characters long!",
                    )
                update_data["password"] = get_password_hash(new_password)

            def set_common_fields(data):
                data["updated_date"] = CURRENT_DATETIME
                data["updated_by"] = user_data.username

            if update_data:
                set_common_fields(update_data)
                db.query(User).filter(User.id == userId).update(update_data)

            db.commit()

            return ok("", "Update password successfully!", HTTP_OK)
        except HTTPException as e:
            db.rollback()
            return formatError("", e.detail, e.status_code)
        except Exception as e:
            db.rollback()
            return formatError("", str(e), HTTP_BAD_REQUEST)
