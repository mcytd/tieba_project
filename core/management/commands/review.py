import time
from django.core.management.base import BaseCommand
from core.models import Post

class Command(BaseCommand):
    help = '循环审核帖子（每5秒检测新待审帖）'

    def handle(self, *args, **options):
        self.stdout.write('审核守护开始（每5秒检查），按 Ctrl+C 退出\n')
        notified_ids = set()
        while True:
            pending = Post.objects.filter(approved=False)
            new_pending = [p for p in pending if p.id not in notified_ids]
            if new_pending:
                self.stdout.write(f'\n🔔 发现 {len(new_pending)} 条新待审帖子：')
                for p in new_pending:
                    self.stdout.write(f'ID:{p.id} | {p.title} | 作者:{p.author} | {p.created_at.strftime("%Y-%m-%d %H:%M")}')
                self.stdout.write('输入帖子ID通过审核（多个用逗号分隔，q 退出，refresh 刷新）：')
                notified_ids.update(p.id for p in new_pending)
                raw = input('>>> ').strip()
                if raw.lower() == 'q':
                    break
                if raw.lower() == 'refresh':
                    continue
                ids = [x.strip() for x in raw.split(',') if x.strip().isdigit()]
                for pid in ids:
                    try:
                        post = Post.objects.get(id=int(pid), approved=False)
                        post.approved = True
                        post.save()
                        self.stdout.write(f'✅ 帖子“{post.title}”已通过审核')
                    except Post.DoesNotExist:
                        self.stdout.write(f'❌ ID {pid} 不存在或已审核')
            else:
                time.sleep(5)
