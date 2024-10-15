from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, FSInputFile, ContentType
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.fsm.context import FSMContext
from keyboards import suggest_post


router = Router()


@router.message(Command('start'))
async def cmd_start(message: Message):
    await message.answer(
            'Для отправки поста в предложку используй "Предложить пост"',
            reply_markup=suggest_post)


class OrderSuggesting(StatesGroup):
    making_post_for_suggest = State()


@router.message(StateFilter(None), F.text.lower() == 'предложить пост')
async def cmd_send(message: Message, state: FSMContext):
    await message.answer(
        'Отправь мне сообщение, текст или видео, которым хочешь поделиться.'
        )

    await state.set_state(OrderSuggesting.making_post_for_suggest)


@router.message(
    OrderSuggesting.making_post_for_suggest,
    F.content_type.in_([ContentType.TEXT, ContentType.PHOTO, ContentType.VIDEO, ContentType.DOCUMENT])
)
async def handle_post(message: Message, state: FSMContext):
    post_data = {}

    if message.caption:
        post_data['text'] = message.caption
    elif message.text:
        post_data['text'] = message.text

    if message.photo:
        post_data['photo'] = message.photo[-1].file_id

    if message.video:
        post_data['video'] = message.video.file_id

    if message.document:
        post_data['document'] = message.document.file_id

    if post_data:
        await state.update_data(post_data=post_data)
        await message.answer('Пост был успешно предложен.')
        await state.set_state(default_state)
    else:
        await message.answer('Не удалось распознать тип данных.')


@router.message(F.text.lower() == 'посмотреть предложку')
async def review_posts(message: Message, state: FSMContext):
    user_data = await state.get_data()
    post_data = user_data.get('post_data')

    if post_data:
        text = post_data.get('text', 'Нет текста')
        photo = post_data.get('photo')
        video = post_data.get('video')
        document = post_data.get('document')

        review_message = f'Предложенный пост:\nТекст: {text}'

        if text:
            pass
            # сохранение текста в бд
        if photo:
            pass
            # сохранение айди фото в бд
        if video:
            pass
            # сохранение айди видео в бд
        if document:
            pass
            # сохранение айди документа в бд
    else:
        await message.answer('Нет предложенных постов.')
