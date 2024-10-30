# community_posts/utils/post_status_manager.py

def update_post_status(post, logger):
    error_statuses = ['pending', 'error', 'error-1', 'error-2', 'error-3', 'error-4', 'error-5']
    if post.status in error_statuses:
        current_index = error_statuses.index(post.status)
        if current_index < len(error_statuses) - 1:
            post.status = error_statuses[current_index + 1]
            logger.info(f'Estado del post actualizado a: {post.status}')
        else:
            post.status = 'error-00'
            logger.info(f'Post ha alcanzado el límite de intentos y se ha marcado como: {post.status}')
