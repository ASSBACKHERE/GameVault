import React, { useEffect, useMemo, useState } from 'react';
import ReactDOM from 'react-dom/client';
import axios from 'axios';
import dayjs from 'dayjs';
import {
  App as AntApp,
  Button,
  Card,
  Col,
  DatePicker,
  Divider,
  Form,
  Input,
  InputNumber,
  Layout,
  Menu,
  Modal,
  Row,
  Select,
  Space,
  Statistic,
  Table,
  Tag,
  Typography,
  message,
} from 'antd';
import {
  BarChartOutlined,
  DashboardOutlined,
  FireOutlined,
  PlusOutlined,
  RocketOutlined,
} from '@ant-design/icons';
import * as echarts from 'echarts';
import './styles.css';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';
const FALLBACK_COVER = 'https://images.unsplash.com/photo-1556438064-2d7646166914?auto=format&fit=crop&w=520&q=80';

type Lookup = { id: number; name: string; color?: string; icon?: string; description?: string };
type Game = {
  id: number;
  title: string;
  original_title?: string;
  cover_url?: string;
  developer?: string;
  publisher?: string;
  release_date?: string;
  description?: string;
  platforms: Lookup[];
  categories: Lookup[];
  tags: Lookup[];
};
type UserGame = {
  id: number;
  status: string;
  priority: string;
  purchase_price: string;
  expected_price: string;
  rating?: string;
  playtime_hours: string;
  review?: string;
  game: Game;
};
type PlaySession = {
  id: number;
  user_game_id: number;
  played_at: string;
  duration_hours: string;
  progress_note?: string;
  note?: string;
};
type UserProfile = {
  id: number;
  username: string;
  email: string;
  nickname?: string;
  avatar_url?: string;
  bio?: string;
  role: string;
};
type Overview = {
  total_games: number;
  wishlist_count: number;
  playing_count: number;
  completed_count: number;
  purchased_count: number;
  total_spent: string;
  total_playtime: string;
};

const api = axios.create({ baseURL: API_BASE_URL });
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('gamevault_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

const statusMap: Record<string, string> = {
  wishlist: '愿望单',
  purchased: '已购买',
  playing: '正在玩',
  completed: '已通关',
  paused: '已搁置',
  dropped: '已放弃',
};

const portalGames = [
  {
    title: 'Elden Ring',
    image: 'https://cdn.akamai.steamstatic.com/steam/apps/1245620/header.jpg',
  },
  {
    title: 'Hades',
    image: 'https://cdn.akamai.steamstatic.com/steam/apps/1145360/header.jpg',
  },
  {
    title: 'Cyberpunk 2077',
    image: 'https://cdn.akamai.steamstatic.com/steam/apps/1091500/header.jpg',
  },
  {
    title: 'Stardew Valley',
    image: 'https://cdn.akamai.steamstatic.com/steam/apps/413150/header.jpg',
  },
  {
    title: 'Hollow Knight',
    image: 'https://cdn.akamai.steamstatic.com/steam/apps/367520/header.jpg',
  },
  {
    title: 'Celeste',
    image: 'https://cdn.akamai.steamstatic.com/steam/apps/504230/header.jpg',
  },
  {
    title: "Baldur's Gate 3",
    image: 'https://cdn.akamai.steamstatic.com/steam/apps/1086940/header.jpg',
  },
  {
    title: 'The Witcher 3',
    image: 'https://cdn.akamai.steamstatic.com/steam/apps/292030/header.jpg',
  },
  {
    title: 'DOOM Eternal',
    image: 'https://cdn.akamai.steamstatic.com/steam/apps/782330/header.jpg',
  },
  {
    title: 'Disco Elysium',
    image: 'https://cdn.akamai.steamstatic.com/steam/apps/632470/header.jpg',
  },
  {
    title: "No Man's Sky",
    image: 'https://cdn.akamai.steamstatic.com/steam/apps/275850/header.jpg',
  },
  {
    title: 'Animal Crossing',
    image: 'https://images.igdb.com/igdb/image/upload/t_cover_big/co3wls.jpg',
  },
];

function Chart({ data, title }: { data: { name: string; value: number }[]; title: string }) {
  const id = useMemo(() => `chart-${Math.random().toString(16).slice(2)}`, []);
  useEffect(() => {
    const instance = echarts.init(document.getElementById(id)!);
    instance.setOption({
      backgroundColor: 'transparent',
      tooltip: { trigger: 'item' },
      title: { text: title, textStyle: { color: '#E5E7EB', fontSize: 15 } },
      series: [
        {
          type: 'pie',
          radius: ['45%', '72%'],
          data,
          label: { color: '#CBD5E1' },
        },
      ],
    });
    return () => instance.dispose();
  }, [data, id, title]);
  return <div id={id} className="chart" />;
}

function TrendChart({ data, title, valueKey }: { data: any[]; title: string; valueKey: string }) {
  const id = useMemo(() => `chart-${Math.random().toString(16).slice(2)}`, []);
  useEffect(() => {
    const instance = echarts.init(document.getElementById(id)!);
    instance.setOption({
      backgroundColor: 'transparent',
      tooltip: { trigger: 'axis' },
      title: { text: title, textStyle: { color: '#E5E7EB', fontSize: 15 } },
      grid: { left: 36, right: 18, top: 58, bottom: 28 },
      xAxis: {
        type: 'category',
        data: data.map((item) => item.month),
        axisLabel: { color: '#94A3B8' },
        axisLine: { lineStyle: { color: '#334155' } },
      },
      yAxis: {
        type: 'value',
        axisLabel: { color: '#94A3B8' },
        splitLine: { lineStyle: { color: 'rgba(148, 163, 184, 0.12)' } },
      },
      series: [
        {
          type: 'line',
          smooth: true,
          data: data.map((item) => item[valueKey]),
          areaStyle: { color: 'rgba(124, 58, 237, 0.18)' },
          lineStyle: { color: '#60A5FA', width: 3 },
          itemStyle: { color: '#A78BFA' },
        },
      ],
    });
    return () => instance.dispose();
  }, [data, id, title, valueKey]);
  return <div id={id} className="chart" />;
}

function AuthPage({ onAuthed }: { onAuthed: () => void }) {
  const [mode, setMode] = useState<'login' | 'register'>('login');
  const [loading, setLoading] = useState(false);
  const [entering, setEntering] = useState(false);

  const submit = async (values: any) => {
    setLoading(true);
    try {
      const path = mode === 'login' ? '/auth/login' : '/auth/register';
      const { data } = await api.post(path, values);
      localStorage.setItem('gamevault_token', data.access_token);
      onAuthed();
    } catch (error: any) {
      message.error(error.response?.data?.detail || '操作失败');
      setEntering(false);
      setLoading(false);
    } finally {
      if (!localStorage.getItem('gamevault_token')) setLoading(false);
    }
  };

  return (
    <div className={`auth-shell ${entering ? 'auth-shell-entering' : ''}`}>
      <div className="star-field" />
      <div className="auth-vignette" />
      <section className="portal-stage" aria-label="GameVault 登录光门">
        <div className="portal-copy">
          <Typography.Title>GameVault</Typography.Title>
        </div>

        <div className="portal-wrap">
          <div className="portal-halo portal-halo-one" />
          <div className="portal-halo portal-halo-two" />
          <div className="portal-core">
            <div className="portal-depth" />
            <div className="portal-rift" />
            <div className="portal-flare" />
          </div>
          <div className="portal-runes">
            {Array.from({ length: 18 }).map((_, index) => (
              <i key={index} style={{ transform: `rotate(${index * 20}deg) translateY(-194px)` }} />
            ))}
          </div>
          {portalGames.map((game, index) => (
            <div className={`flying-cover flying-cover-${index + 1}`} key={game.title}>
              <img src={game.image} alt={game.title} onError={(event) => { event.currentTarget.src = FALLBACK_COVER; }} />
              <span>{game.title}</span>
            </div>
          ))}
        </div>
      </section>

      <Card className="auth-card portal-login-card">
        <div className="login-card-head">
          <div>
            <Typography.Title level={3}>{mode === 'login' ? '玩家登录' : '创建玩家档案'}</Typography.Title>
          </div>
        </div>
        <Form layout="vertical" onFinish={submit} initialValues={{ username: 'demo', password: 'demo123456' }}>
          <div className="login-grid">
            <Form.Item name="username" label="用户名" rules={[{ required: true }]}>
              <Input size="large" disabled={entering} />
            </Form.Item>
            <Form.Item name="password" label="密码" rules={[{ required: true }]}>
              <Input.Password size="large" disabled={entering} />
            </Form.Item>
          </div>
          {mode === 'register' && (
            <div className="login-grid">
              <Form.Item name="email" label="邮箱" rules={[{ required: true, type: 'email' }]}>
                <Input size="large" disabled={entering} />
              </Form.Item>
              <Form.Item name="nickname" label="昵称">
                <Input size="large" disabled={entering} />
              </Form.Item>
            </div>
          )}
          <Button block type="primary" htmlType="submit" loading={loading} size="large" className="portal-submit">
            {mode === 'login' ? '进入 GameVault' : '创建并进入'}
          </Button>
          <Button type="link" block disabled={entering} onClick={() => setMode(mode === 'login' ? 'register' : 'login')}>
            {mode === 'login' ? '没有账号？立即注册' : '已有账号？返回登录'}
          </Button>
        </Form>
      </Card>
    </div>
  );
}

function GameForm({
  open,
  onClose,
  onDone,
  lookups,
  editing,
}: {
  open: boolean;
  onClose: () => void;
  onDone: () => void;
  lookups: { platforms: Lookup[]; categories: Lookup[]; tags: Lookup[] };
  editing?: UserGame | null;
}) {
  const [form] = Form.useForm();

  useEffect(() => {
    if (!open) return;
    if (editing) {
      form.setFieldsValue({
        title: editing.game.title,
        original_title: editing.game.original_title,
        cover_url: editing.game.cover_url,
        developer: editing.game.developer,
        publisher: editing.game.publisher,
        description: editing.game.description,
        status: editing.status,
        priority: editing.priority,
        purchase_price: Number(editing.purchase_price || 0),
        expected_price: Number(editing.expected_price || 0),
        rating: editing.rating ? Number(editing.rating) : undefined,
        playtime_hours: Number(editing.playtime_hours || 0),
        review: editing.review,
        platform_ids: editing.game.platforms.map((item) => item.id),
        category_ids: editing.game.categories.map((item) => item.id),
        tag_ids: editing.game.tags.map((item) => item.id),
      });
    } else {
      form.resetFields();
      form.setFieldsValue({ status: 'wishlist', priority: 'medium' });
    }
  }, [editing, form, open]);

  const submit = async (values: any) => {
    const gamePayload = {
      ...values,
      release_date: values.release_date?.format('YYYY-MM-DD'),
      platform_ids: values.platform_ids || [],
      category_ids: values.category_ids || [],
      tag_ids: values.tag_ids || [],
    };
    if (editing) {
      await api.put(`/games/${editing.game.id}`, gamePayload);
      await api.put(`/user-games/${editing.id}`, {
        status: values.status,
        priority: values.priority,
        purchase_price: values.purchase_price || 0,
        expected_price: values.expected_price || 0,
        rating: values.rating,
        playtime_hours: values.playtime_hours || 0,
        review: values.review,
      });
      message.success('游戏记录已更新');
    } else {
      const { data: game } = await api.post('/games', gamePayload);
      await api.post('/user-games', {
        game_id: game.id,
        status: values.status,
        priority: values.priority,
        purchase_price: values.purchase_price || 0,
        expected_price: values.expected_price || 0,
        rating: values.rating,
        playtime_hours: values.playtime_hours || 0,
        review: values.review,
      });
      message.success('游戏已加入库');
    }
    form.resetFields();
    onDone();
    onClose();
  };

  return (
    <Modal open={open} onCancel={onClose} onOk={() => form.submit()} title={editing ? '编辑游戏记录' : '新增游戏记录'} width={820}>
      <Form form={form} layout="vertical" onFinish={submit} initialValues={{ status: 'wishlist', priority: 'medium' }}>
        <Row gutter={16}>
          <Col span={12}>
            <Form.Item name="title" label="游戏名称" rules={[{ required: true }]}>
              <Input />
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item name="cover_url" label="封面 URL">
              <Input />
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item name="developer" label="开发商">
              <Input />
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item name="publisher" label="发行商">
              <Input />
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item name="release_date" label="发行日期">
              <DatePicker style={{ width: '100%' }} />
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item name="status" label="状态">
              <Select options={Object.entries(statusMap).map(([value, label]) => ({ value, label }))} />
            </Form.Item>
          </Col>
          <Col span={8}>
            <Form.Item name="platform_ids" label="平台">
              <Select mode="multiple" options={lookups.platforms.map((x) => ({ value: x.id, label: x.name }))} />
            </Form.Item>
          </Col>
          <Col span={8}>
            <Form.Item name="category_ids" label="类型">
              <Select mode="multiple" options={lookups.categories.map((x) => ({ value: x.id, label: x.name }))} />
            </Form.Item>
          </Col>
          <Col span={8}>
            <Form.Item name="tag_ids" label="标签">
              <Select mode="multiple" options={lookups.tags.map((x) => ({ value: x.id, label: x.name }))} />
            </Form.Item>
          </Col>
          <Col span={8}>
            <Form.Item name="priority" label="优先级">
              <Select options={[{ value: 'low', label: '低' }, { value: 'medium', label: '中' }, { value: 'high', label: '高' }]} />
            </Form.Item>
          </Col>
          <Col span={8}>
            <Form.Item name="purchase_price" label="购买价格">
              <InputNumber min={0} style={{ width: '100%' }} />
            </Form.Item>
          </Col>
          <Col span={8}>
            <Form.Item name="playtime_hours" label="游玩时长">
              <InputNumber min={0} style={{ width: '100%' }} />
            </Form.Item>
          </Col>
          <Col span={24}>
            <Form.Item name="description" label="游戏简介">
              <Input.TextArea rows={3} />
            </Form.Item>
          </Col>
          <Col span={24}>
            <Form.Item name="review" label="个人评价">
              <Input.TextArea rows={2} />
            </Form.Item>
          </Col>
        </Row>
      </Form>
    </Modal>
  );
}

function Dashboard() {
  const [overview, setOverview] = useState<Overview>();
  const [items, setItems] = useState<UserGame[]>([]);
  const [platforms, setPlatforms] = useState<any[]>([]);
  const [categories, setCategories] = useState<any[]>([]);
  const [statuses, setStatuses] = useState<any[]>([]);
  const [monthlyAdded, setMonthlyAdded] = useState<any[]>([]);
  const [monthlyPlaytime, setMonthlyPlaytime] = useState<any[]>([]);
  const [topRated, setTopRated] = useState<any[]>([]);
  const [topPlaytime, setTopPlaytime] = useState<any[]>([]);
  const [spendingByPlatform, setSpendingByPlatform] = useState<any[]>([]);
  const [sessions, setSessions] = useState<PlaySession[]>([]);
  const [profile, setProfile] = useState<UserProfile>();
  const [lookups, setLookups] = useState({ platforms: [], categories: [], tags: [] } as {
    platforms: Lookup[];
    categories: Lookup[];
    tags: Lookup[];
  });
  const [activeKey, setActiveKey] = useState('dashboard');
  const [open, setOpen] = useState(false);
  const [editing, setEditing] = useState<UserGame | null>(null);
  const [detail, setDetail] = useState<UserGame | null>(null);
  const [sessionOpen, setSessionOpen] = useState(false);
  const [editingSession, setEditingSession] = useState<PlaySession | null>(null);
  const [lookupOpen, setLookupOpen] = useState<'platforms' | 'categories' | 'tags' | null>(null);
  const [libraryView, setLibraryView] = useState<'table' | 'cards'>('table');
  const [q, setQ] = useState('');
  const [statusFilter, setStatusFilter] = useState<string | undefined>();
  const [sessionForm] = Form.useForm();
  const [lookupForm] = Form.useForm();
  const [profileForm] = Form.useForm();

  const load = async () => {
    const [overviewRes, itemsRes, platformRes, categoryRes, statusRes, addedRes, playtimeRes, ratedRes, topPlaytimeRes, spendingRes, sessionsRes, meRes, pRes, cRes, tRes] = await Promise.all([
      api.get('/analytics/overview'),
      api.get('/user-games', { params: { q, status: statusFilter } }),
      api.get('/analytics/platforms'),
      api.get('/analytics/categories'),
      api.get('/analytics/statuses'),
      api.get('/analytics/monthly-added'),
      api.get('/analytics/monthly-playtime'),
      api.get('/analytics/top-rated'),
      api.get('/analytics/top-playtime'),
      api.get('/analytics/spending-by-platform'),
      api.get('/play-sessions'),
      api.get('/auth/me'),
      api.get('/platforms'),
      api.get('/categories'),
      api.get('/tags'),
    ]);
    setOverview(overviewRes.data);
    setItems(itemsRes.data);
    setPlatforms(platformRes.data);
    setCategories(categoryRes.data);
    setStatuses(statusRes.data.map((item: any) => ({ ...item, name: statusMap[item.name] || item.name })));
    setMonthlyAdded(addedRes.data);
    setMonthlyPlaytime(playtimeRes.data);
    setTopRated(ratedRes.data);
    setTopPlaytime(topPlaytimeRes.data);
    setSpendingByPlatform(spendingRes.data);
    setSessions(sessionsRes.data);
    setProfile(meRes.data);
    setLookups({ platforms: pRes.data, categories: cRes.data, tags: tRes.data });
    profileForm.setFieldsValue(meRes.data);
  };

  useEffect(() => {
    load().catch(() => message.error('数据加载失败'));
  }, [q, statusFilter]);

  const updateStatus = async (record: UserGame, status: string) => {
    await api.put(`/user-games/${record.id}`, { status });
    message.success('状态已更新');
    load();
  };

  const remove = async (record: UserGame) => {
    await api.delete(`/user-games/${record.id}`);
    message.success('已删除');
    load();
  };

  const openEditor = (record?: UserGame) => {
    setEditing(record || null);
    setOpen(true);
  };

  const submitSession = async (values: any) => {
    const payload = {
      ...values,
      played_at: values.played_at.format('YYYY-MM-DD'),
      duration_hours: values.duration_hours || 0,
    };
    if (editingSession) {
      await api.put(`/play-sessions/${editingSession.id}`, payload);
      message.success('游玩日志已更新');
    } else {
      await api.post('/play-sessions', payload);
      message.success('游玩日志已添加');
    }
    sessionForm.resetFields();
    setEditingSession(null);
    setSessionOpen(false);
    load();
  };

  const openSessionEditor = (record?: PlaySession) => {
    setEditingSession(record || null);
    if (record) {
      sessionForm.setFieldsValue({
        user_game_id: record.user_game_id,
        played_at: dayjs(record.played_at),
        duration_hours: Number(record.duration_hours || 0),
        progress_note: record.progress_note,
        note: record.note,
      });
    } else {
      sessionForm.resetFields();
    }
    setSessionOpen(true);
  };

  const deleteSession = async (id: number) => {
    await api.delete(`/play-sessions/${id}`);
    message.success('日志已删除');
    load();
  };

  const createLookup = async (values: any) => {
    if (!lookupOpen) return;
    await api.post(`/${lookupOpen}`, values);
    message.success('分类数据已新增');
    lookupForm.resetFields();
    setLookupOpen(null);
    load();
  };

  const deleteLookup = async (kind: 'platforms' | 'categories' | 'tags', id: number) => {
    await api.delete(`/${kind}/${id}`);
    message.success('已删除');
    load();
  };

  const updateProfile = async (values: any) => {
    const { data } = await api.put('/auth/me', values);
    setProfile(data);
    message.success('个人资料已更新');
  };

  const resetDemo = async () => {
    await api.post('/demo/reset');
    message.success('演示数据已重置');
    load();
  };

  const gameColumns = [
    {
      title: '游戏',
      render: (_, record: UserGame) => (
        <Space>
          <img className="cover" src={record.game.cover_url || FALLBACK_COVER} onError={(event) => { event.currentTarget.src = FALLBACK_COVER; }} />
          <div>
            <b>{record.game.title}</b>
            <div className="muted">{record.game.developer || '未知开发商'}</div>
          </div>
        </Space>
      ),
    },
    {
      title: '状态',
      render: (_, record: UserGame) => (
        <Select value={record.status} style={{ width: 110 }} onChange={(value) => updateStatus(record, value)}>
          {Object.entries(statusMap).map(([value, label]) => (
            <Select.Option value={value} key={value}>{label}</Select.Option>
          ))}
        </Select>
      ),
    },
    { title: '优先级', dataIndex: 'priority', render: (value) => <Tag color={value === 'high' ? 'red' : value === 'medium' ? 'blue' : 'default'}>{value}</Tag> },
    { title: '时长', dataIndex: 'playtime_hours', render: (value) => `${value}h` },
    { title: '评分', dataIndex: 'rating', render: (value) => value || '-' },
    {
      title: '操作',
      render: (_, record: UserGame) => (
        <Space>
          <Button type="link" onClick={() => setDetail(record)}>详情</Button>
          <Button type="link" onClick={() => openEditor(record)}>编辑</Button>
          <Button danger type="link" onClick={() => remove(record)}>删除</Button>
        </Space>
      ),
    },
  ];

  const renderStats = () => (
    <Row gutter={[18, 18]}>
      {[
        ['游戏总数', overview?.total_games, '#7C3AED'],
        ['愿望单', overview?.wishlist_count, '#2563EB'],
        ['正在玩', overview?.playing_count, '#22C55E'],
        ['已通关', overview?.completed_count, '#F97316'],
        ['总消费', `¥${overview?.total_spent || 0}`, '#EC4899'],
        ['总时长', `${overview?.total_playtime || 0}h`, '#14B8A6'],
      ].map(([label, value, color]) => (
        <Col span={4} key={label}>
          <Card className="stat-card" style={{ borderColor: `${color}55` }}>
            <Statistic title={label} value={value as any} valueStyle={{ color: color as string }} />
          </Card>
        </Col>
      ))}
    </Row>
  );

  const renderLibrary = (onlyWishlist = false) => (
    <Card title={onlyWishlist ? '愿望单' : '我的游戏库'} className="glass-card">
      <Space className="table-toolbar" wrap>
        <Input.Search placeholder="搜索游戏" allowClear onSearch={setQ} />
        <Select allowClear placeholder="状态筛选" style={{ width: 150 }} onChange={setStatusFilter} options={Object.entries(statusMap).map(([value, label]) => ({ value, label }))} />
        <Select value={libraryView} style={{ width: 130 }} onChange={setLibraryView} options={[{ value: 'table', label: '表格视图' }, { value: 'cards', label: '卡片视图' }]} />
        <Button type="primary" icon={<PlusOutlined />} onClick={() => openEditor()}>新增游戏</Button>
      </Space>
      {libraryView === 'table' ? (
        <Table rowKey="id" dataSource={onlyWishlist ? items.filter((item) => item.status === 'wishlist') : items} pagination={{ pageSize: 8 }} columns={gameColumns as any} />
      ) : (
        <div className="game-card-grid">
          {(onlyWishlist ? items.filter((item) => item.status === 'wishlist') : items).map((item) => (
            <div className="game-card" key={item.id} onClick={() => setDetail(item)}>
              <img src={item.game.cover_url || FALLBACK_COVER} onError={(event) => { event.currentTarget.src = FALLBACK_COVER; }} />
              <div className="game-card-mask">
                <b>{item.game.title}</b>
                <span>{statusMap[item.status]} · {item.playtime_hours}h</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </Card>
  );

  const renderDashboard = () => (
    <>
      {renderStats()}
      <Row gutter={[18, 18]} className="section">
        <Col span={14}>{renderLibrary()}</Col>
        <Col span={10}>
          <Card title="高优先级愿望单" className="glass-card">
            {items.filter((x) => x.status === 'wishlist' || x.priority === 'high').slice(0, 4).map((item) => (
              <div className="wish-item" key={item.id}>
                <img src={item.game.cover_url || FALLBACK_COVER} onError={(event) => { event.currentTarget.src = FALLBACK_COVER; }} />
                <div>
                  <b>{item.game.title}</b>
                  <p>{item.game.description || '暂无简介'}</p>
                  <Space wrap>{item.game.tags.map((tag) => <Tag color={tag.color || 'purple'} key={tag.id}>{tag.name}</Tag>)}</Space>
                </div>
              </div>
            ))}
          </Card>
        </Col>
      </Row>
      <Row gutter={[18, 18]} className="section">
        <Col span={8}><Card className="glass-card"><Chart title="平台分布" data={platforms} /></Card></Col>
        <Col span={8}><Card className="glass-card"><Chart title="类型分布" data={categories} /></Card></Col>
        <Col span={8}><Card className="glass-card"><Chart title="状态分布" data={statuses} /></Card></Col>
      </Row>
    </>
  );

  const renderAnalytics = () => (
    <>
      {renderStats()}
      <Row gutter={[18, 18]} className="section">
        <Col span={12}><Card className="glass-card"><TrendChart title="月度新增游戏" data={monthlyAdded} valueKey="count" /></Card></Col>
        <Col span={12}><Card className="glass-card"><TrendChart title="月度游玩时长" data={monthlyPlaytime} valueKey="hours" /></Card></Col>
        <Col span={8}><Card className="glass-card"><Chart title="平台分布" data={platforms} /></Card></Col>
        <Col span={8}><Card className="glass-card"><Chart title="类型分布" data={categories} /></Card></Col>
        <Col span={8}><Card className="glass-card"><Chart title="状态分布" data={statuses} /></Card></Col>
        <Col span={8}><Card className="glass-card"><Chart title="平台消费占比" data={spendingByPlatform} /></Card></Col>
        <Col span={8}><Card title="评分榜 Top 5" className="glass-card">{topRated.map((item) => <div className="rank-row" key={item.title}><span>{item.title}</span><b>{item.value}</b></div>)}</Card></Col>
        <Col span={8}><Card title="游玩时长榜 Top 5" className="glass-card">{topPlaytime.map((item) => <div className="rank-row" key={item.title}><span>{item.title}</span><b>{item.value}h</b></div>)}</Card></Col>
      </Row>
    </>
  );

  const renderSessions = () => (
    <Card title="游玩日志" className="glass-card" extra={<Button type="primary" onClick={() => openSessionEditor()}>添加日志</Button>}>
      <Table rowKey="id" dataSource={sessions} pagination={{ pageSize: 8 }} columns={[
        { title: '游戏', render: (_, record: PlaySession) => items.find((item) => item.id === record.user_game_id)?.game.title || '-' },
        { title: '日期', dataIndex: 'played_at' },
        { title: '时长', dataIndex: 'duration_hours', render: (value) => `${value}h` },
        { title: '进度', dataIndex: 'progress_note' },
        { title: '备注', dataIndex: 'note' },
        { title: '操作', render: (_, record: PlaySession) => <Space><Button type="link" onClick={() => openSessionEditor(record)}>编辑</Button><Button danger type="link" onClick={() => deleteSession(record.id)}>删除</Button></Space> },
      ] as any} />
    </Card>
  );

  const renderLookup = () => (
    <Row gutter={[18, 18]}>
      {[
        ['platforms', '平台管理', lookups.platforms],
        ['categories', '类型管理', lookups.categories],
        ['tags', '标签管理', lookups.tags],
      ].map(([kind, title, data]: any) => (
        <Col span={8} key={kind}>
          <Card className="glass-card" title={title} extra={<Button size="small" onClick={() => setLookupOpen(kind)}>新增</Button>}>
            <Space wrap>
              {data.map((item: Lookup) => (
                <Tag key={item.id} color={item.color || (kind === 'platforms' ? 'blue' : 'purple')} closable onClose={(event) => { event.preventDefault(); deleteLookup(kind, item.id); }}>
                  {item.name}
                </Tag>
              ))}
            </Space>
          </Card>
        </Col>
      ))}
    </Row>
  );

  const renderProfile = () => (
    <Card title="个人资料" className="glass-card profile-card">
      <Form form={profileForm} layout="vertical" onFinish={updateProfile} initialValues={profile}>
        <Row gutter={16}>
          <Col span={12}><Form.Item label="昵称" name="nickname"><Input /></Form.Item></Col>
          <Col span={12}><Form.Item label="头像 URL" name="avatar_url"><Input /></Form.Item></Col>
          <Col span={24}><Form.Item label="个人简介" name="bio"><Input.TextArea rows={4} /></Form.Item></Col>
        </Row>
        <Button type="primary" htmlType="submit">保存资料</Button>
      </Form>
    </Card>
  );

  const contentMap: Record<string, React.ReactNode> = {
    dashboard: renderDashboard(),
    library: renderLibrary(),
    wishlist: renderLibrary(true),
    sessions: renderSessions(),
    taxonomy: renderLookup(),
    analytics: renderAnalytics(),
    profile: renderProfile(),
  };

  return (
    <Layout className="app-layout">
      <Layout.Sider width={252} className="side">
        <div className="brand">
          <RocketOutlined />
          <span>GameVault</span>
        </div>
        <Menu
          theme="dark"
          mode="inline"
          selectedKeys={[activeKey]}
          onClick={(event) => setActiveKey(event.key)}
          items={[
            { key: 'dashboard', icon: <DashboardOutlined />, label: '首页仪表盘' },
            { key: 'library', icon: <FireOutlined />, label: '我的游戏库' },
            { key: 'wishlist', icon: <RocketOutlined />, label: '愿望单' },
            { key: 'sessions', icon: <FireOutlined />, label: '游玩日志' },
            { key: 'taxonomy', icon: <DashboardOutlined />, label: '分类管理' },
            { key: 'analytics', icon: <BarChartOutlined />, label: '数据统计' },
            { key: 'profile', icon: <RocketOutlined />, label: '个人资料' },
          ]}
        />
      </Layout.Sider>
      <Layout.Content className="content">
        <div className="topbar">
          <div>
            <Typography.Title>游戏愿望单与游玩进度分析系统</Typography.Title>
            <Typography.Text>管理收藏、愿望单、进度、评分和消费数据。</Typography.Text>
          </div>
          <Space>
            <Input.Search placeholder="搜索游戏" allowClear onSearch={setQ} />
            <Button type="primary" icon={<PlusOutlined />} onClick={() => openEditor()}>
              新增游戏
            </Button>
            <Button onClick={resetDemo}>重置演示数据</Button>
            <Button onClick={() => { localStorage.removeItem('gamevault_token'); location.reload(); }}>退出</Button>
          </Space>
        </div>
        {contentMap[activeKey]}

        <GameForm open={open} onClose={() => setOpen(false)} onDone={load} lookups={lookups} editing={editing} />
        <Modal title={detail?.game.title} open={Boolean(detail)} onCancel={() => setDetail(null)} footer={null} width={900} className="detail-drawer-like">
          {detail && (
            <div className="detail-modal">
              <img src={detail.game.cover_url || FALLBACK_COVER} onError={(event) => { event.currentTarget.src = FALLBACK_COVER; }} />
              <div>
                <Typography.Paragraph>{detail.game.description}</Typography.Paragraph>
                <p>开发商：{detail.game.developer || '-'}</p>
                <p>发行商：{detail.game.publisher || '-'}</p>
                <p>状态：{statusMap[detail.status]}</p>
                <p>游玩时长：{detail.playtime_hours}h</p>
                <p>评分：{detail.rating || '-'}</p>
                <p>评价：{detail.review || '-'}</p>
                <Space wrap>{[...detail.game.platforms, ...detail.game.categories, ...detail.game.tags].map((item) => <Tag key={`${item.name}-${item.id}`}>{item.name}</Tag>)}</Space>
              </div>
            </div>
          )}
        </Modal>
        <Modal title={editingSession ? '编辑游玩日志' : '添加游玩日志'} open={sessionOpen} onCancel={() => { setSessionOpen(false); setEditingSession(null); }} onOk={() => sessionForm.submit()}>
          <Form form={sessionForm} layout="vertical" onFinish={submitSession}>
            <Form.Item name="user_game_id" label="游戏" rules={[{ required: true }]}>
              <Select options={items.map((item) => ({ value: item.id, label: item.game.title }))} />
            </Form.Item>
            <Form.Item name="played_at" label="日期" rules={[{ required: true }]}><DatePicker style={{ width: '100%' }} /></Form.Item>
            <Form.Item name="duration_hours" label="游玩时长" rules={[{ required: true }]}><InputNumber min={0.1} style={{ width: '100%' }} /></Form.Item>
            <Form.Item name="progress_note" label="进度"><Input /></Form.Item>
            <Form.Item name="note" label="备注"><Input.TextArea rows={3} /></Form.Item>
          </Form>
        </Modal>
        <Modal title="新增分类数据" open={Boolean(lookupOpen)} onCancel={() => setLookupOpen(null)} onOk={() => lookupForm.submit()}>
          <Form form={lookupForm} layout="vertical" onFinish={createLookup}>
            <Form.Item name="name" label="名称" rules={[{ required: true }]}><Input /></Form.Item>
            {lookupOpen === 'categories' && <Form.Item name="description" label="说明"><Input /></Form.Item>}
            {lookupOpen === 'platforms' && <Form.Item name="icon" label="图标标识"><Input /></Form.Item>}
            {lookupOpen === 'tags' && <Form.Item name="color" label="颜色"><Input placeholder="#7C3AED" /></Form.Item>}
          </Form>
        </Modal>
      </Layout.Content>
    </Layout>
  );
}

function App() {
  const [authed, setAuthed] = useState(Boolean(localStorage.getItem('gamevault_token')));
  return (
    <AntApp>
      {authed ? <Dashboard /> : <AuthPage onAuthed={() => setAuthed(true)} />}
    </AntApp>
  );
}

ReactDOM.createRoot(document.getElementById('root')!).render(<App />);
