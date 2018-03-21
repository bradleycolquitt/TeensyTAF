// As defined here: https://embeddedartistry.com/blog/2017/4/6/circular-buffers-in-cc

typedef struct {
    float * buffer;
    size_t head;
    size_t tail;
    size_t size; //of the buffer
} circular_buf_t;

int circular_buf_reset(circular_buf_t * cbuf);
int circular_buf_put(circular_buf_t * cbuf, float * data);
int circular_buf_get(circular_buf_t * cbuf, float * data);
bool circular_buf_empty(circular_buf_t cbuf);
bool circular_buf_full(circular_buf_t cbuf);
void circular_buf_init(circular_buf_t * cbuf, int size);
