from modelscope.hub.snapshot_download import snapshot_download

snapshot_download("Shanghai_AI_Laboratory/internlm2-chat-1_8b",
                  cache_dir="./",
                  revision='v1.1.0')