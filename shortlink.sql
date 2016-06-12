-- phpMyAdmin SQL Dump
-- version 4.5.4.1deb2ubuntu1
-- http://www.phpmyadmin.net
--
-- Host: localhost:3306
-- Generation Time: 2016-06-13 00:45:43
-- 服务器版本： 5.7.12-0ubuntu1
-- PHP Version: 7.0.4-7ubuntu2.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `shortlink`
--
CREATE DATABASE IF NOT EXISTS `shortlink` DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci;
USE `shortlink`;

-- --------------------------------------------------------

--
-- 表的结构 `urls`
--

DROP TABLE IF EXISTS `urls`;
CREATE TABLE `urls` (
  `id` int(11) NOT NULL,
  `tag` varchar(16) COLLATE utf8_unicode_ci NOT NULL,
  `url` text COLLATE utf8_unicode_ci NOT NULL,
  `rt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- 转存表中的数据 `urls`
--

INSERT INTO `urls` (`id`, `tag`, `url`, `rt`) VALUES
(1, 'index', 'http://www.baidu.com', '2016-06-12 15:11:07'),
(2, 'subscribe', 'http://chenjiehua.me', '2016-06-12 16:25:39'),
(3, 'test', 'https%3A%2F%2Fgithub.com%2Fjkbrzt%2Fhttpie', '2016-06-12 16:33:08'),
(4, 'test1', 'https%3A%2F%2Fgithub.com%2Fjkbrzt%2Fhttpie', '2016-06-12 16:35:16'),
(5, '594frXbf', 'http%3A%2F%2Fchenjiehua.me', '2016-06-12 16:36:32'),
(6, '42eG9TuS', 'http%3A%2F%2Fchenjiehua2.me', '2016-06-12 16:39:28');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `urls`
--
ALTER TABLE `urls`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `tag` (`tag`);

--
-- 在导出的表使用AUTO_INCREMENT
--

--
-- 使用表AUTO_INCREMENT `urls`
--
ALTER TABLE `urls`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
