from django.http import JsonResponse
from django.utils import timezone

from posts.models import Post
from .models import Comment

# 댓글 목록
def get_comments(post_id):
    comments = Comment.objects.filter(post=post_id).order_by('-created_at')
    comments_list = []
    for comment in comments:
        comments_list.append({
            'id': comment.id,
            'content': comment.content,
            'created_by': comment.created_by.first_name,
            'updated_by': comment.updated_by.first_name,
            'created_at': comment.created_at.astimezone(timezone.get_current_timezone()).strftime('%Y-%m-%d %H:%M'),
            'updated_at': comment.updated_at.astimezone(timezone.get_current_timezone()).strftime('%Y-%m-%d %H:%M'),
        })
    return comments_list

# 댓글 등록
def create_comment(request):
    if not request.user.is_authenticated:
        return JsonResponse({'result': 'error', 'message': '로그인 후 이용해주세요.'})
    
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        if not post_id:
            return JsonResponse({'result': 'error', 'message': '게시글을 선택해주세요.'})
        
        post = Post.objects.get(id=post_id)        
        if not post:
            return JsonResponse({'result': 'error', 'message': '게시글을 찾을 수 없습니다.'})
        
        content = request.POST.get('content')          
        if not content:
            return JsonResponse({'result': 'error', 'message': '댓글 내용을 입력해주세요.'})
        
        # 댓글 등록
        comment = Comment(
            post=post,
            content=content,
            created_by=request.user,
            updated_by=request.user
        )
        comment.save()
        
        # 댓글 목록
        comments = get_comments(post_id)

        return JsonResponse({'result': 'success', 'comments': comments})

# 댓글 수정
def update_comment(request, comment_id):
    if not request.user.is_authenticated:
        return JsonResponse({'result': 'error', 'message': '로그인 후 이용해주세요.'})
    
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        if not post_id:
            return JsonResponse({'result': 'error', 'message': '게시글을 선택해주세요.'})
        
        post = Post.objects.get(id=post_id)        
        if not post:
            return JsonResponse({'result': 'error', 'message': '게시글을 찾을 수 없습니다.'})
        
        content = request.POST.get('content')          
        if not content:
            return JsonResponse({'result': 'error', 'message': '댓글 내용을 입력해주세요.'})
        
        comment_id = request.POST.get('comment_id')
        if not comment_id:
            return JsonResponse({'result': 'error', 'message': '댓글을 선택해주세요.'})
        
        comment = Comment.objects.get(id=comment_id)
        if not comment:
            return JsonResponse({'result': 'error', 'message': '댓글을 찾을 수 없습니다.'})
        
        if comment.created_by != request.user:
            return JsonResponse({'result': 'error', 'message': '댓글 수정 권한이 없습니다.'})
        
        # 댓글 수정
        comment.content = content
        comment.updated_by = request.user
        comment.save()

        # 댓글 목록
        comments = get_comments(post_id)

        return JsonResponse({'result': 'success', 'comments': comments})


#댓글삭제
def delete_comment(request, comment_id):
    if not request.user.is_authenticated:
        return JsonResponse({'result': 'error', 'message': '로그인 후 이용해주세요.'})

    if request.method == 'POST':
        post_id = request.POST.get('post_id')  # AJAX 요청에서 넘어오는 데이터 확인
        if not post_id:
            return JsonResponse({'result': 'error', 'message': '게시글을 선택해주세요.'})

        # 게시글 확인
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return JsonResponse({'result': 'error', 'message': '게시글을 찾을 수 없습니다.'})

        # 댓글 확인
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return JsonResponse({'result': 'error', 'message': '댓글을 찾을 수 없습니다.'})

        # 댓글 작성자 확인
        if comment.created_by != request.user:
            return JsonResponse({'result': 'error', 'message': '댓글 삭제 권한이 없습니다.'})

        # 댓글 삭제
        comment.delete()

        # 최신 댓글 목록 반환
        comments = get_comments(post_id)
        return JsonResponse({'result': 'success', 'comments': comments})

    return JsonResponse({'result': 'error', 'message': '잘못된 요청입니다.'})
