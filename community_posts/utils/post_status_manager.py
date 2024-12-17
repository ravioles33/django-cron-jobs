# community_posts/utils/post_status_manager.py

def update_post_status(post, logger):
    # La cadena de errores ahora va directamente desde 'pending' a 'error-1',
    # luego 'error-2', 'error-3', 'error-4' y finalmente 'error-5'.
    # Ya no existe 'error' ni 'error-00'.
    error_statuses = ['pending', 'error-1', 'error-2', 'error-3', 'error-4', 'error-5']

    if post.status in error_statuses:
        current_index = error_statuses.index(post.status)
        # Si está en 'pending', pasa a 'error-1' en el siguiente intento fallido.
        # Luego 'error-2', 'error-3', 'error-4', y finalmente 'error-5'.
        if current_index < len(error_statuses) - 1:
            post.status = error_statuses[current_index + 1]
            logger.info(f'Estado del post actualizado a: {post.status}')
        else:
            # Ya en error-5 no se avanza más.
            logger.info(f'El post ya se encuentra en {post.status} y no se reintentará más.')
    else:
        logger.warning(f'El estado {post.status} no está contemplado en la cadena de errores.')
